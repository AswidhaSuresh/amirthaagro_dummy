# app/utils/helpers.py
# ------------------------------------------------------------
# Reusable utility/helper functions across the application
# ------------------------------------------------------------

import os
import secrets
import string
import pandas as pd
from datetime import datetime


# ---------- 🔒 General Utility Methods ----------
class helpers:
    @staticmethod
    def ensure_directory_exists(path):
        """
        Ensure the specified directory exists, create if not.
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def mask_email(email):
        """
        Mask an email address for secure logging (e.g. j***@mail.com)
        """
        parts = email.split("@")
        if len(parts) != 2:
            return email
        local, domain = parts
        return f"{local[0]}***@{domain}"

    @staticmethod
    def generate_password(length=4):
        """
        Generates a secure numeric-only password of given length.
        """
        return ''.join(secrets.choice(string.digits) for _ in range(length))


# ---------- 📊 Stock Excel Parser ----------
class StockParseError(Exception):
    """Raised when critical issues occur during Excel stock parsing."""
    pass


class StockParser:
    @staticmethod
    def clean_str(value):
        """Returns clean string or empty if blank, '-', or 'N/A'."""
        if pd.isna(value):
            return ""
        val = str(value).strip()
        return "" if val.upper() in ["-", "N/A", "NA"] else val

    @staticmethod
    def clean_float(value):
        """Returns float or None from Excel cell."""
        try:
            val = str(value).strip()
            return None if val.upper() in ["", "-", "N/A", "NA"] else float(val)
        except:
            return None

    @staticmethod
    def clean_int(value):
        """Returns int or None from Excel cell."""
        try:
            val = str(value).strip()
            return None if val.upper() in ["", "-", "N/A", "NA"] else int(float(val))
        except:
            return None

    @staticmethod
    def parse_excel_date(value):
        """Safely parse Excel date fields."""
        try:
            return pd.to_datetime(value, dayfirst=True).date()
        except:
            return None

    @staticmethod
    def extract_stock_data(filepath: str) -> list[dict]:
        """
        Extracts structured stock data from Excel and raises critical errors for API use.

        Args:
            filepath (str): Path to the Excel file.

        Returns:
            List[dict]: Cleaned list of stock records.

        Raises:
            StockParseError: On any critical structure issue.
        """
        try:
            xls = pd.ExcelFile(filepath)
            df = xls.parse(xls.sheet_names[0], header=None, keep_default_na=False)
        except Exception as e:
            raise StockParseError(f"❌ Failed to open or parse Excel file: {str(e)}")

        records = []
        current_party = None

        for idx, row in df.iterrows():
            first_cell = str(row[0]).strip().upper()

            # Detect party name row
            if str(row[0]).strip() and not str(row[1]).strip() and not str(row[2]).strip():
                if "TOTAL" not in first_cell:
                    current_party = ' '.join(str(row[0]).strip().lower().split())
                    current_party = current_party.title()
                continue

            # Skip known junk/header/total rows
            if first_cell in ["PARTY TOTAL", "S NO", ""]:
                continue

            if current_party is None:
                raise StockParseError(f"❌ Missing party name before row {idx + 1}")

            # Must start with a valid S.No
            try:
                s_no = int(row[0])
            except (ValueError, TypeError):
                continue  # skip non-numeric rows

            try:
                record = {
                    "party_name": current_party,
                    "s_no": s_no,
                    "bank": StockParser.clean_str(row[1]),
                    "lot_no": StockParser.clean_str(row[2]),
                    "date": StockParser.parse_excel_date(row[3]),
                    "mark": StockParser.clean_str(row[4]),
                    "lorry": StockParser.clean_str(row[5]),
                    "product": StockParser.clean_str(row[6]),
                    "packing": StockParser.clean_float(row[7]),
                    "quantity": StockParser.clean_int(row[8]),
                    "weight_kgs": StockParser.clean_float(row[9]),
                    "chamber": StockParser.clean_str(row[10]),
                    "floor": StockParser.clean_str(row[11]),
                    "bayee": StockParser.clean_str(row[12]),
                }

                if not record["lot_no"] or not record["product"]:
                    raise StockParseError(f"❌ Missing 'lot_no' or 'product' at row {idx + 1}")

                records.append(record)

            except Exception as e:
                raise StockParseError(f"❌ Failed to parse row {idx + 1}: {str(e)}")

        if not records:
            raise StockParseError("❌ No valid stock records found in the file.")

        return records


# ---------- 🧪 Debug Usage ----------
if __name__ == "__main__":
    try:
        filepath = "amirtha stock details.xlsx"
        data = StockParser.extract_stock_data(filepath)
        print(f"✅ Extracted {len(data)} rows:")
        for row in data:
            print(row)
    except StockParseError as e:
        print(f"ERROR: {e}")
