import csv


def ascii_to_swapped_hex_pairs(text: str):
    hex_str = text.encode("ascii").hex().upper()
    bytes_list = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    pairs = []
    for i in range(0, len(bytes_list), 2):
        b1 = bytes_list[i]
        b2 = bytes_list[i + 1] if i + 1 < len(bytes_list) else "00"
        pairs.append("H" + b2 + b1)

    return pairs


def generate_csv(text, start_register=3000, step_size=2, step_start=2):

    with open("plc_output_Barcode.csv", mode="w", newline="") as file:
        writer = csv.writer(file)

        # Headers
        writer.writerow(["Step", "LineStarter", "Cmd", "Value"])

        hex_pairs = ascii_to_swapped_hex_pairs(text)

        current_reg = start_register
        current_step = step_start

        # ---- First Row (LD SM400) ----
        writer.writerow([current_step, "", "LD", "SM400"])

        current_step += step_size

        # ---- Data Rows ----
        for val in hex_pairs:

            # MOV row
            writer.writerow([current_step, "", "MOV", val])

            # Register row
            writer.writerow(["", "", "", f"D{current_reg}"])

            current_reg += 1
            current_step += step_size + 2

    print("✅ CSV generated: plc_output_final8.csv")


# ================== INPUT ==================
text = """SIZE 42.5 mm, 35 mm
GAP 3 mm, 0 mm
DIRECTION 0,0
REFERENCE 0,0
OFFSET 0 mm
SET PEEL OFF
SET CUTTER OFF
SET PARTIAL_CUTTER OFF
SET TEAR ON
CLS
CODEPAGE 1252
TEXT 314,254,"ROMAN.TTF",180,1,7,"60% BACK BASE (-) STR--------------"
TEXT 314,224,"ROMAN.TTF",180,1,6,"PART NO"
TEXT 232,224,"ROMAN.TTF",180,1,6,"-"
TEXT 214,224,"ROMAN.TTF",180,1,6,"E2MS46300"
TEXT 314,195,"ROMAN.TTF",180,1,6,"DATE"
TEXT 232,195,"ROMAN.TTF",180,1,6,"-"
TEXT 214,195,"ROMAN.TTF",180,1,6,"09 04 26"
TEXT 314,166,"ROMAN.TTF",180,1,6,"SR NO"
TEXT 232,166,"ROMAN.TTF",180,1,6,"-"
TEXT 214,166,"ROMAN.TTF",180,1,6,"000008"
TEXT 314,138,"ROMAN.TTF",180,1,6,"CODE"
TEXT 232,138,"ROMAN.TTF",180,1,6,"-"
TEXT 214,138,"ROMAN.TTF",180,1,6,"DAE002"
TEXT 79,223,"ROMAN.TTF",180,1,6,"S202"
TEXT 110,198,"ROMAN.TTF",180,1,6,"SHIFT"
TEXT 47,198,"ROMAN.TTF",180,1,6,"A"
TEXT 114,168,"ROMAN.TTF",180,1,6,"FIREWALL OK"
BAR 123,119, 3, 106
QRCODE 216,108,L,3,A,180,M2,S7,"E2MS-46300-0008-090426"
TEXT 273,39,"ROMAN.TTF",180,1,6,"E2MS-46300-0008-090426"
PRINT 1,1
"""

generate_csv(text=text, start_register=1000, step_size=2, step_start=0)
