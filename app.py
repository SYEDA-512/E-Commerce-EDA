import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce EDA", layout="wide")

# --- Title ---
st.title("📊 E-Commerce Dataset Explorer")

# --- File uploader ---
uploaded_file = st.file_uploader("C:/Users/User/OneDrive/Documents/ecommerce_dataset.csv", type=["csv"])

if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file, low_memory=False)

    # --- Show dataset preview ---
    st.subheader("Dataset Preview")
    st.write(df.head())

    # --- Summary statistics ---
    st.subheader("Summary Statistics")
    st.write(df.describe(include="all"))

    # --- Missing values ---
    st.subheader("Missing Values")
    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Values"]
    st.write(missing[missing["Missing Values"] > 0])

    # --- Correlation heatmap ---
    st.subheader("Correlation Heatmap")
    num_cols = df.select_dtypes(include="number")
    if not num_cols.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(num_cols.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # --- Numeric distribution plots ---
    st.subheader("Numeric Distributions")
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        selected_num = st.selectbox("Select a numeric column:", num_cols)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[selected_num].dropna(), bins=30, kde=True, ax=ax)
        st.pyplot(fig)

    # --- Categorical column plots ---
    st.subheader("Top Categories")
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    if cat_cols:
        selected_cat = st.selectbox("Select a categorical column:", cat_cols)
        top_cats = df[selected_cat].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=top_cats.values, y=top_cats.index, ax=ax)
        ax.set_xlabel("Count")
        ax.set_ylabel(selected_cat)
        st.pyplot(fig)

else:
    st.info("👆 Upload a CSV file to begin")
