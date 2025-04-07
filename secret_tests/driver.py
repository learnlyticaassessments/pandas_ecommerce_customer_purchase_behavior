import pandas as pd
import importlib.util
import os
import random

def test_student_code(solution_path):
    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    results = []
    failures = set()

    # 🔐 Anti-Cheat: Use random input to verify dynamic logic
    try:
        rand_purchases = [
            [random.randint(1000, 2000), "ItemA", 1, 100.0],
            [random.randint(1000, 2000), "ItemB", 2, 200.0],
            [random.randint(1000, 2000), "ItemC", 1, 300.0],
        ]
        df = student_module.create_purchase_df(rand_purchases)

        # Must contain at least 3 rows
        if not isinstance(df, pd.DataFrame) or df.shape[0] < 3:
            raise Exception("create_purchase_df failed structure check")
    except Exception:
        failures.add("create_purchase_df")

    try:
        # Anti-cheat for repeat detection
        repeat_df = student_module.get_repeat_customers(
            pd.DataFrame([
                [111, "Item1", 1, 100.0],
                [222, "Item2", 2, 200.0],
                [111, "Item3", 1, 150.0],
            ], columns=["CustomerID", "Product", "Quantity", "TotalAmount"])
        )
        if not isinstance(repeat_df, pd.DataFrame) or "PurchaseCount" not in repeat_df.columns:
            raise Exception("Repeat buyer output invalid")

        if repeat_df.shape[0] != 1 or repeat_df.iloc[0]["CustomerID"] != 111:
            raise Exception("Repeat logic mismatch")

    except Exception:
        failures.add("get_repeat_customers")

    try:
        # Anti-cheat for spend calculation
        spend_df = student_module.calculate_total_spend(
            pd.DataFrame([
                [111, "Item1", 1, 100.0],
                [222, "Item2", 2, 200.0],
                [111, "Item3", 1, 150.0],
            ], columns=["CustomerID", "Product", "Quantity", "TotalAmount"])
        )
        if not isinstance(spend_df, pd.DataFrame) or "TotalSpent" not in spend_df.columns:
            raise Exception("Spend output invalid")
        if spend_df[spend_df["CustomerID"] == 111]["TotalSpent"].values[0] != 250.0:
            raise Exception("Spend logic failed")
    except Exception:
        failures.add("calculate_total_spend")

    # Now test with fixed cases
    try:
        df = student_module.create_purchase_df([
            [401, "Shoes", 1, 2500.0],
            [402, "T-Shirt", 2, 1200.0],
            [401, "Watch", 1, 3500.0]
        ])
        if df.shape == (3, 4) and list(df.columns) == ["CustomerID", "Product", "Quantity", "TotalAmount"]:
            results.append("✅ TC1: Creating structured purchase DataFrame")
        else:
            raise Exception()
    except:
        results.append("❌ TC1: Creating structured purchase DataFrame failed")

    try:
        df = student_module.create_customer_df([
            [401, "Alice", "Mumbai"],
            [402, "Bob", "Delhi"]
        ])
        if df.shape == (2, 3) and "CustomerName" in df.columns:
            results.append("✅ TC2: Creating customer profile DataFrame")
        else:
            raise Exception()
    except:
        results.append("❌ TC2: Creating customer profile DataFrame failed")

    try:
        purchase_df = pd.DataFrame([
            [401, "Shoes", 1, 2500.0],
            [402, "T-Shirt", 2, 1200.0]
        ], columns=["CustomerID", "Product", "Quantity", "TotalAmount"])
        customer_df = pd.DataFrame([
            [401, "Alice", "Mumbai"],
            [402, "Bob", "Delhi"]
        ], columns=["CustomerID", "CustomerName", "Location"])
        merged = student_module.merge_customer_info(purchase_df, customer_df)
        if isinstance(merged, pd.DataFrame) and merged.shape == (2, 6):
            results.append("✅ TC3: Merging customer info into purchase data")
        else:
            raise Exception()
    except:
        results.append("❌ TC3: Merging customer info into purchase data failed")

    try:
        df = pd.DataFrame([
            [401, "Shoes", 1, 2500.0],
            [402, "T-Shirt", 2, 1200.0],
            [401, "Watch", 1, 3500.0]
        ], columns=["CustomerID", "Product", "Quantity", "TotalAmount"])
        repeat = student_module.get_repeat_customers(df)
        if "get_repeat_customers" in failures:
            raise Exception("Hardcoded / logic violation")
        if repeat.shape[0] == 1 and repeat.iloc[0]["CustomerID"] == 401:
            results.append("✅ TC4: Identifying repeat buyers")
        else:
            raise Exception()
    except:
        results.append("❌ TC4: Identifying repeat buyers failed")

    try:
        df = pd.DataFrame([
            [401, "Shoes", 1, 2500.0],
            [402, "T-Shirt", 2, 1200.0],
            [401, "Watch", 1, 3500.0]
        ], columns=["CustomerID", "Product", "Quantity", "TotalAmount"])
        spend = student_module.calculate_total_spend(df)
        if "calculate_total_spend" in failures:
            raise Exception("Hardcoded / logic violation")
        expected = {401: 6000.0, 402: 1200.0}
        passed = all(spend.set_index("CustomerID").loc[k, "TotalSpent"] == v for k, v in expected.items())
        if passed:
            results.append("✅ TC5: Calculating total spend per customer")
        else:
            raise Exception()
    except:
        results.append("❌ TC5: Calculating total spend per customer failed")

    print("\n".join(results))

    report_path = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "report.txt")
   
def write_report(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py"))
    test_student_code(path)
