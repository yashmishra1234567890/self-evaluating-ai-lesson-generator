
from database.connection import get_connection


def create_tables():
    """
    Create all required SQLite database tables.

    Tables:
        1. runs
        2. evaluation_logs
        3. learning_memory
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------
        # TABLE 1: RUNS
        # ----------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runs (

                run_id TEXT PRIMARY KEY,

                topic TEXT NOT NULL,

                status TEXT NOT NULL DEFAULT 'in_progress'
                    CHECK (
                        status IN (
                            'in_progress',
                            'shipped',
                            'rejected',
                            'system_error'
                        )
                    ),

                total_attempts INTEGER DEFAULT 0
                    CHECK (total_attempts BETWEEN 0 AND 3),

                final_lesson_content TEXT,

                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ----------------------------------
        # TABLE 2: EVALUATION LOGS
        # ----------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_logs (

                log_id INTEGER PRIMARY KEY AUTOINCREMENT,

                run_id TEXT NOT NULL,

                attempt_number INTEGER NOT NULL
                    CHECK (attempt_number BETWEEN 1 AND 3),

                draft_content TEXT NOT NULL,

                passed_checkpoint_ids TEXT NOT NULL DEFAULT '[]'
                    CHECK (json_valid(passed_checkpoint_ids)),

                failed_checkpoint_ids TEXT NOT NULL DEFAULT '[]'
                    CHECK (json_valid(failed_checkpoint_ids)),

                evaluator_feedback_json TEXT NOT NULL
                    CHECK (json_valid(evaluator_feedback_json)),

                is_passing INTEGER NOT NULL
                    CHECK (is_passing IN (0, 1)),

                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (run_id)
                    REFERENCES runs(run_id)
                    ON DELETE CASCADE,

                UNIQUE (run_id, attempt_number)
            )
        """)

        # ----------------------------------
        # TABLE 3: LEARNING MEMORY
        # ----------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_memory (

                memory_id INTEGER PRIMARY KEY AUTOINCREMENT,

                checkpoint_id TEXT UNIQUE NOT NULL,

                total_failure_count INTEGER NOT NULL DEFAULT 0
                    CHECK (total_failure_count >= 0),

                historical_guidance TEXT NOT NULL,

                last_triggered_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ----------------------------------
        # CREATE INDEXES
        # ----------------------------------

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_runs_status
            ON runs(status)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluation_run_id
            ON evaluation_logs(run_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_learning_failure_count
            ON learning_memory(total_failure_count DESC)
        """)

        connection.commit()

        print("Database tables created successfully!")

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()
