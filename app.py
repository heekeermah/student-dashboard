import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
df = pd.read_excel(r'C:\Users\USER\Downloads\student1.xlsx')

# Check dataset info
df.info()
print(df.head())

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Student Performance Dashboard", style={"textAlign": "center"}),

    html.Label("Select Student:"),
    dcc.Dropdown(
        id="student-dropdown",
        options=[{"label": name, "value": name} for name in df["Name"]],
        value=df["Name"].iloc[0],  # Default to first student
        style={"width": "50%"}
    ),

    dcc.Graph(id="subject-score-graph"),
    html.H3("Student Performance Table"),
    html.Div(id="data-table")
])


# Callback to update dashboard
@app.callback(
    [Output("subject-score-graph", "figure"),
     Output("data-table", "children")],
    [Input("student-dropdown", "value")]
)
def update_dashboard(selected_student):
    print(f"Selected student: {selected_student}")

    # Filter data for selected student
    student_data = df[df["Name"] == selected_student]

    if student_data.empty:
        return {}, html.Div("No data available")

    # Subjects and scores
    subjects = ["Maths", "English", "ss", "HE", "Bstudies", "BST", "Computer", "Agric", "IRS"]
    scores = [student_data[subject].values[0] for subject in subjects]
    highest_scores = {subject: df[subject].max() for subject in subjects}
    average_score = sum(scores) / len(scores)

    # Bar chart
    fig = px.bar(
        x=subjects,
        y=scores,
        title=f"{selected_student}'s Subject Scores",
        labels={"x": "Subjects", "y": "Scores"},
        color=scores,
        color_continuous_scale="Viridis"
    )

    # Table
    table = html.Table([
        html.Thead(html.Tr([html.Th("Subject"), html.Th("Student Score"), html.Th("Highest Score")])),
        html.Tbody([
            html.Tr([html.Td(subject),
                     html.Td(student_data[subject].values[0]),
                     html.Td(highest_scores[subject])])
            for subject in subjects
        ]),
        html.Tbody([
            html.Tr([html.Td("Average Score"), html.Td(average_score)]),
            html.Tr([html.Td("Punctuality"), html.Td(student_data["Punctuality"].values[0])]),
            html.Tr([html.Td("Attendance"), html.Td(student_data["Attendance(%)"].values[0])])
        ])
    ], style={"width": "50%", "margin": "auto", "border": "1px solid black", "textAlign": "center"})

    return fig, table


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
