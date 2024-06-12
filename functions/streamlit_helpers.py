import streamlit as st

def forecast_column(col_index, forecast_df):
    st.markdown(f"""<p style='padding-top: 40px;'><b>{forecast_df.columns[col_index]}</b></p>""", unsafe_allow_html=True)
    img_path = f"https:{forecast_df.iloc[-2, col_index]}"
    st.markdown(
        f"""
        <div style='padding: 0px; margin-top:-15px;'>
            <img src='{img_path}' alt='Weather Icon'>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"""<p style='padding-top: 0px;'>{forecast_df.iloc[1, col_index]} °F</p>""", unsafe_allow_html=True)
    st.markdown(f"""<p style='padding-top: 0px;'>{forecast_df.iloc[3, col_index]} °F</p>""", unsafe_allow_html=True)
    st.markdown(f"""<p style='padding-top: 0px;'>{forecast_df.iloc[-7, col_index]}%</p>""", unsafe_allow_html=True)
    st.markdown(f"""<p style='padding-top: 0px;'>{forecast_df.iloc[6, col_index]} mph</p>""", unsafe_allow_html=True)