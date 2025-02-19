import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import json

def init(file):
    df = pd.read_csv(file, low_memory=False)
    df["SCORE"] = pd.to_numeric(df["SCORE"], errors="coerce")
    df["MEMBERS"] = pd.to_numeric(df["MEMBERS"], errors="coerce")
    df = df[df["MEMBERS"] > 0]
    df["GENRES"] = df["GENRES"].str.replace("'", '"')
    df["GENRES"] = df["GENRES"].astype(str).str.replace('\D+', '')
    df["GENRES"] = df["GENRES"].apply(clean_and_parse)
    df["GENRES"] = df["GENRES"].apply(lambda genre_list: [d["name"] for d in genre_list] if isinstance(genre_list, list) else [])
    df["START_DATE"] = pd.to_datetime(df["START_DATE"], format="%Y-%m-%d", errors="coerce")
    return df

def clean_and_parse(entry):
    entry = entry.strip()
    
    if entry == "" or entry == "[]" or entry == "{}":
        return []
    
    if not entry.startswith("[") and not entry.endswith("]"):
        return [{"name": entry}]

    return json.loads(entry)

def contains_isekai(genres):
    return "Isekai" in str(genres)
    
def test(file):
    df = init(file)
    print(df.head())
    
def score_over_time(file):
    df = init(file)
    df = df.dropna(subset=["START_DATE", "SCORE", "MEMBERS"])
    
    df["LOG_MEMBERS"] = np.log(df["MEMBERS"] + 1)
    tickvals = np.linspace(df["LOG_MEMBERS"].min(), df["LOG_MEMBERS"].max(), num=6)
    ticktext = [f"{int(np.exp(val)):,}" for val in tickvals]
    
    fig = px.scatter(
        df,
        x="START_DATE",
        y="SCORE",
        color="LOG_MEMBERS",
        labels={
            "START_DATE": "Start Date",
            "SCORE": "Mean Score",
            "LOG_MEMBERS": "Log(Members)"
            },
        hover_data={"TITLE": True, "MEMBERS": True, "LOG_MEMBERS": False},
        opacity=0.6,
        template="plotly_dark",
        color_continuous_scale="Plasma",
    )
    
    fig.update_traces(marker={'size': 7})
    
    fig.update_layout(
        font=dict(
            family="Roboto",
            size=15
        ),
        coloraxis_colorbar=dict(
            title="Members",
            tickvals=tickvals,
            ticktext=ticktext,
            title_font=dict(size=20, family="Roboto Medium"),
            title_side="top"
        ),
        title=dict(
            text="MAL Anime Scores Over Time",
            x=0.5,
            xanchor='center',
            font={
                'size':25,
                'family':"Roboto Black"
            },
        ),
        xaxis_title_font=dict(size=20, family="Roboto Medium"),
        yaxis_title_font=dict(size=20, family="Roboto Medium"),
    )
    
    fig.write_html("plots/mal_score_over_time_member_colored.html")
    
def score_over_members(file):
    df = init(file)
    df = df.dropna(subset=["TITLE", "SCORE", "MEMBERS", "START_DATE"])
    df = df[df['START_DATE'] >= '1960-01-01']
    df["LOG_MEMBERS"] = np.log(df["MEMBERS"] + 1)
    df['START_TIMESTAMP'] = df['START_DATE'].astype(np.int64)
    df["START_TIMESTAMP"] = df["START_TIMESTAMP"] - df["START_TIMESTAMP"].min()
    
    fig = px.scatter(
        df,
        x="LOG_MEMBERS",
        y="SCORE",
        color="START_TIMESTAMP",
        labels={
            "MEMBERS": "Members",
            "SCORE": "Mean Score",
            },
        hover_data={"TITLE": True, "SCORE": True, "MEMBERS": True},
        opacity=0.6,
        template="plotly_dark",
        color_continuous_scale="Agsunset"
    )
    
    fig.update_traces(marker={'size': 7})
    
    fig.update_layout(
        font=dict(
            family="Roboto",
            size=15
        ),
        title=dict(
            text="MAL Scores vs. Members, Date-colored",
            x=0.5,
            xanchor='center',
            font={
                'size':25,
                'family':"Roboto Black"
            },
        ),
        coloraxis_colorbar=dict(
            title="Date",
            title_font=dict(size=20, family="Roboto Medium"),
            title_side="top",
            tickvals=[]
        ),
        xaxis_title_font=dict(size=20, family="Roboto Medium"),
        xaxis_title=dict(text="Ln(Members)"),
        yaxis_title_font=dict(size=20, family="Roboto Medium"),
        yaxis_title=dict(text="Score"),
        showlegend=False
    )
    
    fig.write_html("plots/mal_score_over_members_date_colored.html")
    
    
    
def score_members_isekai(file):
    df = init(file)
    df = df.dropna(subset=["TITLE", "GENRES", "SCORE", "MEMBERS"])
    
    df["ISEKAI"] = df["GENRES"].apply(lambda x: "Isekai" if contains_isekai(x) else "Other")
    df["MARKER_SIZE"] = df["ISEKAI"].apply(lambda x: 6 if x == "Isekai" else 2)
    
    fig = px.scatter(
        df,
        x="MEMBERS",
        y="SCORE",
        color="ISEKAI",
        labels={
            "MEMBERS": "Members",
            "SCORE": "Mean Score",
            },
        hover_data={"TITLE": True, "SCORE": True, "MEMBERS": True, "GENRES": False},
        opacity=0.6,
        template="plotly_dark",
        color_discrete_map={"Isekai": "#dfff00", "Other": "#f57fcc"},
        size="MARKER_SIZE"
    )
    
    fig.update_layout(
        font=dict(
            family="Roboto",
            size=15
        ),
        title=dict(
            text="MAL Scores vs. Members, Isekai-colored",
            x=0.5,
            xanchor='center',
            font={
                'size':25,
                'family':"Roboto Black"
            },
        ),
        legend=dict(
            title="Genre",
            font=dict(size=20, family="Roboto Medium")
        ),
        xaxis=dict(
            type="log",
            tickmode="array",
            tickvals=[10**i for i in range(6)],
            ticktext=[f"{int(10**i):,}" for i in range(6)]
        ),
        xaxis_title_font=dict(size=20, family="Roboto Medium"),
        yaxis_title_font=dict(size=20, family="Roboto Medium"),
    )
    
    fig.write_html("plots/mal_score_over_members_isekai_colored.html")
    
def isekai_members_double_gaussian(file):
    df = init(file)
    df = df.dropna(subset=["MEMBERS", "GENRES"])
    df["LOG_MEMBERS"] = np.log(df["MEMBERS"] + 1)
    
    df["ISEKAI"] = df["GENRES"].apply(lambda x: "Isekai" if contains_isekai(x) else "Other")
    
    isekai_data = df[df["ISEKAI"] == "Isekai"]["LOG_MEMBERS"]
    non_isekai_data = df[df["ISEKAI"] == "Other"]["LOG_MEMBERS"]
    
    colors = ['#2BCDC1', '#F66095']
    hist_data = [isekai_data, non_isekai_data]
    group_labels = ["Isekai", "Not Isekai"]
    
    fig = ff.create_distplot(
        hist_data, 
        group_labels,
        colors=colors,
        bin_size=0.5,
        curve_type='normal'
        )
    
    fig.update_layout(
        template="plotly_dark",
        font=dict(
            family="Roboto",
            size=15
        ),
        legend=dict(
            title="Genre",
            font=dict(size=20, family="Roboto Medium")
        ),
        title=dict(
            text="Popularity of Isekais vs. Non-Isekais on MAL",
            x=0.5,
            xanchor='center',
            font={
                'size':25,
                'family':"Roboto Black"
            },
        ),
    )
    
    fig.write_html("plots/mal_isekai_popularity_double_gaussian.html")

def isekai_score_double_gaussian(file):
    df = init(file)
    df = df.dropna(subset=["SCORE", "GENRES"])
    
    df["ISEKAI"] = df["GENRES"].apply(lambda x: "Isekai" if contains_isekai(x) else "Other")
    
    isekai_data = df[df["ISEKAI"] == "Isekai"]["SCORE"]
    non_isekai_data = df[df["ISEKAI"] == "Other"]["SCORE"]
    
    colors = ['#2BCDC1', '#F66095']
    hist_data = [isekai_data, non_isekai_data]
    group_labels = ["Isekai", "Not Isekai"]
    
    fig = ff.create_distplot(
        hist_data, 
        group_labels,
        colors=colors,
        bin_size=0.5,
        curve_type='normal'
        )
    
    fig.update_layout(
        template="plotly_dark",
        font=dict(
            family="Roboto",
            size=15
        ),
        legend=dict(
            title="Genre",
            font=dict(size=20, family="Roboto Medium")
        ),
        title=dict(
            text="Score of Isekais vs. Non-Isekais on MAL",
            x=0.5,
            xanchor='center',
            font={
                'size':25,
                'family':"Roboto Black"
            },
        ),
    )
    
    fig.write_html("plots/mal_isekai_score_double_gaussian.html")
    
def isekai_members_double_histogram(file):
    df = init(file)
    df = df.dropna(subset=["MEMBERS", "GENRES"])
    df["LOG_MEMBERS"] = np.log(df["MEMBERS"] + 1)
    
    df["ISEKAI"] = df["GENRES"].apply(lambda x: "Isekai" if contains_isekai(x) else "Other")
    
    fig = px.histogram(
        df,
        x="LOG_MEMBERS",
        title="Histogram of Isekai vs. Non-Isekai anime on MAL",
        color="ISEKAI",
        category_orders={"ISEKAI": ["Non-Isekai", "Isekai"]},
        color_discrete_map={"Other": "#00798C", "Isekai": "#D1495B"},
        log_y=True
    )
    
    fig.update_layout(
        template="plotly_dark",
        font=dict(
            family="Roboto",
            size=15
        ),
        legend=dict(
            title="Genre",
            font=dict(size=20, family="Roboto Medium")
        ),
        title=dict(
            x=0.5,
            xanchor='center',
            font={
                'size':25,
                'family':"Roboto Black"
            },
        ),
        xaxis_title_font=dict(size=20, family="Roboto Medium"),
        xaxis_title=dict(text="Ln(Members)"),
        yaxis_title_font=dict(size=20, family="Roboto Medium"),
        yaxis_title=dict(text="Log(Count)"),
    )
    
    fig.write_html("plots/mal_isekai_popularity_double_histogram.html")