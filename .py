import os
import sys
import sqlite3


def generate_tree(root="."):
    """Generate a directory tree as text."""
    lines = []
    for dirpath, dirnames, filenames in os.walk(root):
        depth = dirpath.count(os.sep) - root.count(os.sep)
        indent = "    " * depth

        if dirpath == root:
            lines.append(".")
        else:
            lines.append(f"{indent}{os.path.basename(dirpath)}/")

        subindent = "    " * (depth + 1)
        for f in sorted(filenames):
            lines.append(f"{subindent}{f}")

    return "\n".join(lines)


def collect_all_files(root="."):
    """Collect all files recursively."""
    results = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            results.append(os.path.join(dirpath, name))
    return sorted(results)


def read_db_first_row(path):
    """Extract the first row from any table inside the .db file."""
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        # Find tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()

        if not tables:
            return "[DB has no tables]"

        table = tables[0][0]

        # Read first row
        cur.execute(f"SELECT * FROM {table} LIMIT 1")
        row = cur.fetchone()

        if row is None:
            return f"[DB table '{table}' has no rows]"

        # Convert tuple to readable string
        return f"[DB first row from table '{table}']: {row}"

    except Exception as e:
        return f"[DB read error: {e}]"
    finally:
        try:
            conn.close()
        except:
            pass


def merge_with_tree_and_db(output_file, root="."):
    tree_text = generate_tree(root)

    with open(output_file, "w", encoding="utf-8") as out:
        # 1. Directory tree
        out.write("===== DIRECTORY TREE =====\n")
        out.write(tree_text)
        out.write("\n\n===== FILE CONTENTS =====\n\n")

        # 2. All files content
        for path in collect_all_files(root):
            if os.path.abspath(path) == os.path.abspath(output_file):
                continue

            out.write(f"{path}:\n")

            # Case: DB file
            if path.lower().endswith(".db"):
                out.write(read_db_first_row(path))
                out.write("\n\n")
                continue

            # Case: normal text file
            try:
                with open(path, "r", encoding="utf-8") as f:
                    out.write(f.read())
            except UnicodeDecodeError:
                out.write("[Skipped: binary or non-text file]\n")
            except Exception as e:
                out.write(f"[Error reading file: {e}]\n")

            out.write("\n")

    print(f"Done! Output saved to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        output = sys.argv[1]
    else:
        output = "merged_with_tree.txt"

    merge_with_tree_and_db(output)
