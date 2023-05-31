import plotly_express as px
import pandas as pd
import streamlit as st
from helper_func import data_parser, utils
import numpy as np
from streamlit_extras.annotated_text import annotated_text


def trend_chart(data, freq):
    data = data.assign(
        registration_date=data["registration_date"].dt.strftime("%B, %Y")
    )
    tab1, tab2 = st.tabs(["Visualize Charts", "View Dataframe"])
    with tab1:
        if (
            st.radio(
                "Select Chart Type",
                options=["Bar Chart", "Line Chart"],
                horizontal=True,
            )
            == "Bar Chart"
        ):
            fig = px.bar(
                data,
                x="registration_date",
                y="number_of_registrations",
                template="presentation",
                title=f"Number of Registrations by {freq}",
            )
        else:
            fig = px.line(
                data,
                x="registration_date",
                y="number_of_registrations",
                template="presentation",
                title=f"Number of Registrations by {freq}",
            )
        fig.update_layout(
            showlegend=False,
            hovermode="x",
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Rockwell"),
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        download_data = utils.convert_df(data)
        st.download_button(
            "Download Data",
            data=download_data,
            file_name=f"reg_by_{freq}.csv",
            mime="text/csv",
        )
        st.dataframe(data, use_container_width=True)


def grouped_chart(data: pd.DataFrame, group_by: str):
    title_text = group_by.replace("_", " ").title()
    grp_df = (
        data.groupby(by=[group_by])
        .agg(number_of_registrations=("product_id", "count"))
        .reset_index()
    )
    grp_df = grp_df.sort_values(by="number_of_registrations", ascending=False)
    tab1, tab2 = st.tabs(["Visualize Charts", "View Dataframe"])

    with tab1:
        num1, num2 = st.columns([1, 1])
        with num1:
            order = st.selectbox(
                f"{title_text} Sort Order",
                options=["Top", "Bottom"],
                key=f"{group_by}_1",
            )
            order_ = True if order == "Bottom" else False

        with num2:
            num_fal = st.selectbox(
                f"Number of {title_text}(s) to Show",
                options=[10, 20, 40, 100],
                key=f"{group_by}_2",
            )

        grp_df = grp_df.sort_values(by="number_of_registrations", ascending=order_)[
            :num_fal
        ]

        line1 = st.empty()
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        # contribution

        top_value = grp_df["number_of_registrations"].sum()
        num_grps = grp_df[group_by].nunique()
        avg = np.round(top_value / num_grps)
        med = np.percentile(grp_df["number_of_registrations"], 50)
        min_value = grp_df["number_of_registrations"].min()
        max_value = grp_df["number_of_registrations"].max()

        overall = data["registration_number"][
            data["registration_number"] != "Not Specified"
        ].count()
        perc = np.round(top_value / overall * 100)
        line1.markdown(
            f"""##### The {order} {num_fal} {title_text} Contributed :green[{perc}% ({data_parser.human_format(top_value)})] of the Total Registrations :green[({data_parser.human_format(overall)})]"""
        )

        with col1:
            annotated_text(
                "Average Value: ",
                (f"{data_parser.human_format(avg)}", "value", "#83c9ff"),
            )

        with col2:
            annotated_text(
                "Median Value: ",
                (f"{data_parser.human_format(med)}", "value", "#83c9ff"),
            )

        with col3:
            annotated_text(
                "Least Value: ",
                (f"{data_parser.human_format(min_value)}", "value", "#83c9ff"),
            )

        with col4:
            annotated_text(
                "Maximum Value: ",
                (f"{data_parser.human_format(max_value)}", "value", "#83c9ff"),
            )

        text_values = [
            data_parser.human_format(x) for x in grp_df.number_of_registrations
        ]
        grp_df[group_by] = grp_df[group_by].str.slice(0, 20)
        fig = px.bar(
            grp_df,
            x=group_by,
            y="number_of_registrations",
            color=group_by,
            template="presentation",
            text=text_values,
            hover_name=group_by,
            title=f"Number of Registrations by {title_text}",
        )
        fig.update_layout(
            showlegend=False,
            hovermode="x",
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Rockwell"),
        )

        fig.update_traces(hovertemplate="%{x} <br> Number of Registrations = %{y}")
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        download_data = utils.convert_df(grp_df)
        st.download_button(
            "Download Data",
            data=download_data,
            file_name="reg_by_category.csv",
            mime="text/csv",
            key=f"{group_by}",
        )
        st.dataframe(grp_df, use_container_width=True)
