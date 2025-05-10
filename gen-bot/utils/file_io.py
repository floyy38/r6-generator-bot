def get_account(path):
    try:
        with open(path, "r") as f:
            lines = f.readlines()

        if not lines:
            return None

        # Look for a valid email:password line
        for i, line in enumerate(lines):
            if ":" in line:
                account = line.strip()
                del lines[i]
                with open(path, "w") as f:
                    f.writelines(lines)
                return account

        print(f"[get_account] No valid account found in {path}")
        return None

    except Exception as e:
        print(f"[get_account] Error reading {path}: {e}")
        return None

def count_accounts(path):
    try:
        with open(path, "r") as f:
            return sum(1 for line in f if ":" in line)
    except Exception as e:
        print(f"[count_accounts] Error reading {path}: {e}")
        return 0
