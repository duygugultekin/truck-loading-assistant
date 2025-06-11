import pandas as pd


data = {
    "products": [
        {
            "Code": "159",
            "Width": 61.0,
            "Length": 67.0,
            "Quantity": 25,
            "City": "Ankara - Beypazarı",
            "Rotated": True,
            "Height": 211.0,
            "Max Stack Count": 2
        },
        {
            "Code": "089",
            "Width": 162.6,
            "Length": 75.2,
            "Quantity": 6,
            "City": "Ankara - Beypazarı",
            "Rotated": True,
            "Height": 93.2,
            "Max Stack Count": 3
        },
        {
            "Code": "774",
            "Width": 66.0,
            "Length": 67.7,
            "Quantity": 15,
            "City": "Ankara - Beypazarı",
            "Rotated": True,
            "Height": 188.2,
            "Max Stack Count": 2
        },
        {
            "Code": "089",
            "Width": 162.6,
            "Length": 75.2,
            "Quantity": 2,
            "City": "Ankara - Altındağ",
            "Rotated": True,
            "Height": 93.2,
            "Max Stack Count": 3
        },
        {
            "Code": "022",
            "Width": 91.6,
            "Length": 75.2,
            "Quantity": 2,
            "City": "Ankara - Altındağ",
            "Rotated": True,
            "Height": 89.3,
            "Max Stack Count": 3
        },
        {
            "Code": "030",
            "Width": 123.1,
            "Length": 75.2,
            "Quantity": 2,
            "City": "Ankara - Altındağ",
            "Rotated": True,
            "Height": 89.3,
            "Max Stack Count": 3
        },
        {
            "Code": "031",
            "Width": 157.1,
            "Length": 75.2,
            "Quantity": 2,
            "City": "Ankara - Altındağ",
            "Rotated": True,
            "Height": 89.3,
            "Max Stack Count": 3
        },
        {
            "Code": "988",
            "Width": 61.0,
            "Length": 67.0,
            "Quantity": 10,
            "City": "Kars - Merkez",
            "Rotated": True,
            "Height": 209.0,
            "Max Stack Count": 2
        },
        {
            "Code": "043",
            "Width": 123.1,
            "Length": 75.2,
            "Quantity": 4,
            "City": "Ardahan - Göle",
            "Rotated": True,
            "Height": 89.3,
            "Max Stack Count": 3
        },
        {
            "Code": "044",
            "Width": 157.1,
            "Length": 75.2,
            "Quantity": 4,
            "City": "Ardahan - Göle",
            "Rotated": True,
            "Height": 89.3,
            "Max Stack Count": 3
        }
    ]
}

#  Creating DataFrame
df = pd.DataFrame(data["products"])

# Volume Calculations
df["Volume"] = df["Width"] * df["Length"] * df["Height"] * df["Quantity"]

# Printing General Table
print("📦 Product Table:\n")
print(df)

# Group Summary Information
summary = df.groupby("City").agg(
    Total_Quantity=("Quantity", "sum"),
    Average_Height=("Height", "mean"),
    Total_Volume=("Volume", "sum")
).reset_index()

print("\n📊 City Based Summary Table:\n")
print(summary)
