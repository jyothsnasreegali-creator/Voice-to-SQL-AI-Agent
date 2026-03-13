import sqlalchemy
from sqlalchemy import create_engine, text
import ollama
import json

MODEL_ID = 'qwen2.5-coder:7b' 

def get_schema_subset(engine) -> str:
    try:
        inspector = sqlalchemy.inspect(engine)
        schema_info = []
        for table_name in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns(table_name)]
            schema_info.append(f"Table: {table_name} (Columns: {', '.join(columns)})")
        return "\n".join(schema_info) if schema_info else "The database is empty."
    except Exception as e:
        return f"Schema Error: {e}"

def build_sql_agent(db_uri: str = "sqlite:///sales.db"):
    engine = create_engine(db_uri)
    schema = get_schema_subset(engine)
    return {"engine": engine, "schema": schema}

def query(agent_context, user_question):
    engine = agent_context["engine"]
    schema = agent_context["schema"]

    prompt = f"""
    You are a Senior SQLite Expert. 
    Current Schema: {schema}
    Request: "{user_question}"
    Respond ONLY with JSON: {{"sql": "...", "summary": "..."}}
    """

    try:
        response = ollama.chat(model=MODEL_ID, messages=[{'role': 'user', 'content': prompt}])
        content = response['message']['content'].strip()
        
        # Robust JSON extraction
        start, end = content.find('{'), content.rfind('}') + 1
        res_data = json.loads(content[start:end])
        raw_sql = res_data.get('sql', '')

        data_rows = []
        with engine.connect() as conn:
            # Split and execute multiple queries (e.g., CREATE then INSERT)
            queries = [q.strip() for q in raw_sql.split(';') if q.strip()]
            for q in queries:
                res = conn.execute(text(q).execution_options(autocommit=True))
                # If it's a SELECT, grab the data
                if q.upper().startswith("SELECT"):
                    data_rows = [dict(row._mapping) for row in res.fetchall()]
            conn.commit()

        agent_context["schema"] = get_schema_subset(engine)
        return {"summary": res_data.get('summary', 'Done!'), "data": data_rows}

    except Exception as e:
        return {"summary": f"Error: {str(e)[:50]}", "data": []}