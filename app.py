import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and file upload
st.title("Recruitment Data Dashboard")
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

# Only proceed if a file is uploaded
if uploaded_file is not None:
    # Load the data from the uploaded file
    data = pd.read_csv(uploaded_file)
    
    # Show the original dataset
    st.header("Original Dataset")
    st.dataframe(data)
    
    # Display total number of contacts in the original dataset
    st.write(f"**Total Contacts in Original Dataset:** {len(data)}")
    
    # Remove duplicates based on 'phone number' column
    data_deduped = data.drop_duplicates(subset=['phone number'])
    
    # Display total number of unique contacts after removing duplicates
    st.write(f"**Total Unique Contacts after Deduplication:** {len(data_deduped)}")
    
    st.header("Dataset after Removing Duplicates")
    st.dataframe(data_deduped)
    
    # Add download button for deduplicated data
    csv = data_deduped.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Deduplicated Data as CSV",
        data=csv,
        file_name="deduplicated_data.csv",
        mime="text/csv"
    )
    
    # Count of numbers based on different recruiters
    recruiter_counts = data_deduped['recruiter'].value_counts()
    
    # Visualization 1: Count of numbers based on different recruiters
    st.header("Count of Numbers by Recruiter")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=recruiter_counts.index, y=recruiter_counts.values, ax=ax, palette="viridis")
    ax.set_title("Total Numbers by Recruiter")
    ax.set_xlabel("Recruiter")
    ax.set_ylabel("Number of Contacts")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Visualization 2: Contacts by WhatsApp Group
    group_counts = data['group name'].value_counts()
    st.header("Count of Contacts by WhatsApp Group")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=group_counts.index, y=group_counts.values, ax=ax, palette="magma")
    ax.set_title("Contacts by WhatsApp Group")
    ax.set_xlabel("WhatsApp Group")
    ax.set_ylabel("Number of Contacts")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Additional Insight: Top 5 Recruiters by Unique Contacts
    top_recruiters = recruiter_counts.head(5)
    st.header("Top 5 Recruiters by Unique Contacts")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top_recruiters.index, y=top_recruiters.values, ax=ax, palette="coolwarm")
    ax.set_title("Top 5 Recruiters by Unique Contacts")
    ax.set_xlabel("Recruiter")
    ax.set_ylabel("Unique Contacts")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Filter Data Table by Recruiter
    st.sidebar.subheader("Filter by Recruiter")
    selected_recruiter = st.sidebar.selectbox("Choose a recruiter", options=data['recruiter'].unique())
    filtered_data = data[data['recruiter'] == selected_recruiter]
    st.write(f"Data for Recruiter: {selected_recruiter}")
    st.dataframe(filtered_data)
    
    # Insights Summary
    st.header("Summary of Insights")
    st.write(f"**Total Contacts in Original Dataset:** {len(data)}")
    st.write(f"**Total Unique Contacts after Deduplication:** {len(data_deduped)}")
    st.write(f"**Total Unique Recruiters:** {data['recruiter'].nunique()}")
    st.write(f"**Most Contacts are from the WhatsApp Group:** '{group_counts.idxmax()}' with {group_counts.max()} contacts.")
else:
    st.write("Please upload a CSV file to proceed.")
