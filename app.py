import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

foods = pd.read_excel("foods.csv.xlsx")
foods.columns = foods.columns.str.strip()

formulations = pd.read_excel("formulations.xlsx.xlsx")


def get_product_values(product):

    product_data = formulations[
        formulations["Product"].str.lower()
        ==
        product.lower()
    ]

    if len(product_data) == 0:
        return None

    total_protein = 0
    total_fat = 0
    total_carbs = 0
    total_fiber = 0
    total_calcium = 0
    total_iron = 0
    total_cost = 0

    for i in range(1,5):

        ingredient = str(
            product_data.iloc[0][f"Ingredient{i}"]
        ).lower().strip()

        percentage = product_data.iloc[0][f"P{i}"]

        if ingredient == "-":
            continue

        food_data = foods[
            foods["foods"].str.lower().str.strip()
            ==
            ingredient
        ]

        if len(food_data) == 0:
            continue

        total_protein += (
            food_data.iloc[0]["protein"]
            * percentage / 100
        )

        total_fat += (
            food_data.iloc[0]["fat"]
            * percentage / 100
        )

        total_carbs += (
            food_data.iloc[0]["carbs"]
            * percentage / 100
        )

        total_fiber += (
            food_data.iloc[0]["fiber"]
            * percentage / 100
        )

        total_calcium += (
            food_data.iloc[0]["Calcium"]
            * percentage / 100
        )

        total_iron += (
            food_data.iloc[0]["iron"]
            * percentage / 100
        )

        total_cost += (
            food_data.iloc[0]["cost"]
            * percentage / 100
        )

    return {
        "Protein": round(total_protein,2),
        "Fat": round(total_fat,2),
        "Carbs": round(total_carbs,2),
        "Fiber": round(total_fiber,2),
        "Calcium": round(total_calcium,2),
        "Iron": round(total_iron,2),
        "Cost": round(total_cost,2)
    }
def food_search(food):

    result = foods[
        foods["foods"].str.lower().str.strip()
        ==
        food.lower().strip()
    ]

    if len(result) == 0:
        return "Food Not Found"

    return f"""
Protein : {result.iloc[0]['protein']} g

Fat : {result.iloc[0]['fat']} g

Carbs : {result.iloc[0]['carbs']} g

Fiber : {result.iloc[0]['fiber']} g

Calcium : {result.iloc[0]['Calcium']} mg

Iron : {result.iloc[0]['iron']} mg

Cost : ₹{result.iloc[0]['cost']}/kg
"""
def product_search(product):

    values = get_product_values(product)

    if values is None:
        return "Product Not Found"

    return f"""
Protein : {values['Protein']} g

Fat : {values['Fat']} g

Carbs : {values['Carbs']} g

Fiber : {values['Fiber']} g

Calcium : {values['Calcium']} mg

Iron : {values['Iron']} mg

Cost : ₹{values['Cost']}/kg
"""
def compare_products(product1, product2):

    p1 = get_product_values(product1)
    p2 = get_product_values(product2)

    if p1 is None:
        return f"{product1} Not Found"

    if p2 is None:
        return f"{product2} Not Found"

    return f"""
PRODUCT COMPARISON

Protein:
{p1['Protein']} g vs {p2['Protein']} g

Fat:
{p1['Fat']} g vs {p2['Fat']} g

Carbs:
{p1['Carbs']} g vs {p2['Carbs']} g

Fiber:
{p1['Fiber']} g vs {p2['Fiber']} g

Calcium:
{p1['Calcium']} mg vs {p2['Calcium']} mg

Iron:
{p1['Iron']} mg vs {p2['Iron']} mg

Cost:
₹{p1['Cost']} vs ₹{p2['Cost']}
"""
def recommend_products(goal):

    goal = goal.lower()

    results = []

    for product in formulations["Product"]:

        values = get_product_values(product)

        if values is None:
            continue

        results.append(
            (
                product,
                values
            )
        )

    if goal == "protein":

        results = sorted(
            results,
            key=lambda x:
            x[1]["Protein"],
            reverse=True
        )

    elif goal == "fiber":

        results = sorted(
            results,
            key=lambda x:
            x[1]["Fiber"],
            reverse=True
        )

    elif goal == "calcium":

        results = sorted(
            results,
            key=lambda x:
            x[1]["Calcium"],
            reverse=True
        )

    else:

        return """
Enter:

protein

fiber

or

calcium
"""

    output = ""

    for product, values in results[:5]:

        output += (
            f"{product}"
            f" | "
            f"{goal.capitalize()}: "
            f"{values[goal.capitalize()]}\n"
        )

    return output
def generate_report(product):

    values = get_product_values(product)

    if values is None:
        return None

    import pandas as pd

    report = pd.DataFrame({

        "Parameter": [
            "Protein",
            "Fat",
            "Carbs",
            "Fiber",
            "Calcium",
            "Iron",
            "Cost"
        ],

        "Value": [
            values["Protein"],
            values["Fat"],
            values["Carbs"],
            values["Fiber"],
            values["Calcium"],
            values["Iron"],
            values["Cost"]
        ]

    })

    filename = (
        product.replace(" ", "_")
        + "_Report.xlsx"
    )

    report.to_excel(
        filename,
        index=False
    )

    return filename
def fssai_claim_checker(product):

    values = get_product_values(product)

    if values is None:
        return "Product Not Found"

    protein = values["Protein"]

    if protein >= 12:

        return f"""
PRODUCT : {product}

PROTEIN : {protein} g

FSSAI CLAIM:
✅ HIGH PROTEIN
"""

    elif protein >= 6:

        return f"""
PRODUCT : {product}

PROTEIN : {protein} g

FSSAI CLAIM:
✅ SOURCE OF PROTEIN
"""

    else:

        return f"""
PRODUCT : {product}

PROTEIN : {protein} g

❌ NO PROTEIN CLAIM ALLOWED
"""
def nutrition_label(product):

    values = get_product_values(product)

    if values is None:
        return "Product Not Found"

    return f"""
==================================

        NUTRITION FACTS

==================================

Product : {product}

Protein  : {values['Protein']} g

Fat      : {values['Fat']} g

Carbs    : {values['Carbs']} g

Fiber    : {values['Fiber']} g

Calcium  : {values['Calcium']} mg

Iron     : {values['Iron']} mg

==================================
"""
import matplotlib.pyplot as plt
def nutrition_dashboard():

    products = []

    protein = []
    fat = []
    carbs = []
    fiber = []

    for product in formulations["Product"]:

        values = get_product_values(product)

        if values is not None:

            products.append(product)

            protein.append(values["Protein"])
            fat.append(values["Fat"])
            carbs.append(values["Carbs"])
            fiber.append(values["Fiber"])

    plt.figure(figsize=(12,6))

    x = range(len(products))

    plt.plot(
        x,
        protein,
        marker="o",
        label="Protein"
    )

    plt.plot(
        x,
        fat,
        marker="o",
        label="Fat"
    )

    plt.plot(
        x,
        carbs,
        marker="o",
        label="Carbs"
    )

    plt.plot(
        x,
        fiber,
        marker="o",
        label="Fiber"
    )

    plt.xticks(
        x,
        products,
        rotation=90
    )

    plt.ylabel("Nutrient Value (g)")
    plt.xlabel("Products")
    plt.title("Nutrition Dashboard")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "nutrition_dashboard.png"
    )

    return "nutrition_dashboard.png"
home_tab = gr.Interface(

    fn=lambda: """
AI FOOD PRODUCT ASSISTANT

Developed By:
V. Ratna Varshini

Department:
Food Technology

Features:
✓ Food Search
✓ Product Calculator
✓ Product Comparison
✓ Product Recommendation
✓ Dashboard Analytics
✓ Excel Report Generator
✓ FSSAI Claims
✓ Nutrition Label Generator

 Project Status:
Phase 1 Completed
Phase 2 Website Development
""", 
    inputs=None,

    outputs="text",

    title="Home"

)
compare_tab = gr.Interface(
    fn=compare_products,

    inputs=[
        gr.Textbox(
            label="Product 1"
        ),
        gr.Textbox(
            label="Product 2"
        )
    ],

    outputs=gr.Textbox(
        label="Comparison Result"
    ),

    title="Product Comparison",

    description="Compare nutrition and cost of two products."
)
recommend_tab = gr.Interface(

    fn=recommend_products,

    inputs=gr.Dropdown(
        [
            "protein",
            "fiber",
            "calcium"
        ],
        label="Select Goal"
    ),

    outputs=gr.Textbox(
        label="Recommended Product"
    ),

    title="Product Recommendation",

    description="Get top products based on nutrition goal."
)
report_tab = gr.Interface(

    fn=generate_report,

    inputs=gr.Textbox(
        label="Product Name"
    ),

    outputs=gr.File(
        label="Download Report"
    ),

    title="Excel Report Generator",

    description="Generate downloadable nutrition reports."

)
claim_tab = gr.Interface(

    fn=fssai_claim_checker,

    inputs=gr.Textbox(
        label="Enter Product Name"
    ),

    outputs=gr.Textbox(
        label="FSSAI Claim Result"
    ),

    title="FSSAI Claim Checker",

    description="Check Protein Claims as per FSSAI."
)
label_tab = gr.Interface(

    fn=nutrition_label,

    inputs=gr.Textbox(
        label="Enter Product Name"
    ),

    outputs=gr.Textbox(
        label="Nutrition Label"
    ),

    title="Nutrition Label Generator",

    description="Generate Nutrition Facts Label."
)
dashboard_tab = gr.Interface(

    fn=nutrition_dashboard,

    inputs=None,

    outputs=gr.Image(),

    title=" Nutrition Dashboard",

    description="Protein Analysis Dashboard"

)
food_tab = gr.Interface(

    fn=food_search,

    inputs=gr.Textbox(
        label="Enter Food Name",
        placeholder="Example: ragi"
    ),

    outputs=gr.Textbox(
        label="Nutrition Information"
    ),

    title="Food Nutrition Search",

    description="Search nutritional information of food ingredients."

)
product_tab = gr.Interface(

    fn=product_search,

    inputs=gr.Textbox(
        label="Enter Product Name",
        placeholder="Example: High Protein Cookie"
    ),

    outputs=gr.Textbox(
        label="Product Analysis"
    ),

    title="Product Nutrition Calculator",

    description="Calculate nutrition and cost of formulated food products."

)


app = gr.TabbedInterface(

    [

        home_tab,
        food_tab,
        product_tab,
        compare_tab,
        recommend_tab,
        dashboard_tab,
        report_tab,
        claim_tab,
        label_tab

    ],

    [

        "🏠 Home",
        "🔍 Food Search",
        "📊 Product Calculator",
        "⚖️ Comparison",
        "🎯 Recommendation",
        "📈 Dashboard",
        "📄 Reports",
        "✅ FSSAI Claims",
        "🏷️ Nutrition Label"

    ]
)
app.launch(
    share=True
    )