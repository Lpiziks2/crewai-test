import streamlit as st
import os
import pandas as pd
from tempfile import NamedTemporaryFile
import time
from main import run_eda_on_file

def main():
    st.set_page_config(page_title="EDA Tool", page_icon="📊", layout="wide")
    
    st.title("📊 Automated Exploratory Data Analysis Tool")
    st.markdown("""
    Upload a CSV file and get comprehensive exploratory data analysis with recommendations.
    This tool uses CrewAI to perform:
    - Statistical analysis
    - Data visualization
    - Cleaning recommendations
    """)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Create a preview of the data
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.subheader("Data Preview")
            st.dataframe(df_preview.head(5))
            
            # Display basic info
            st.subheader("Basic Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", df_preview.shape[0])
            with col2:
                st.metric("Columns", df_preview.shape[1])
            with col3:
                st.metric("Missing Values", df_preview.isna().sum().sum())
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Button to start analysis
            if st.button("Run Exploratory Data Analysis"):
                with st.spinner("Running analysis... This may take a few minutes."):
                    # Create a temporary file from the uploaded file
                    with NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Run the EDA pipeline
                    try:
                        start_time = time.time()
                        result = run_eda_on_file(tmp_path)
                        elapsed_time = time.time() - start_time
                        
                        st.success(f"Analysis completed in {elapsed_time:.2f} seconds!")
                        
                        # Get the report file path from the result and convert to absolute path
                        report_path = os.path.abspath(result.strip())
                        
                        # Read the report content from the file
                        with open(report_path, 'r') as f:
                            report_content = f.read()
                        
                        # Display the report content
                        st.subheader("EDA Report")
                        st.markdown(report_content, unsafe_allow_html=True)
                        
                        # Download button for the report
                        st.download_button(
                            label="Download Report",
                            data=report_content,
                            file_name=f"eda_report_{time.strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                    
                    finally:
                        # Clean up the temporary file
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)
        
        except Exception as e:
            st.error(f"Error reading the CSV file: {str(e)}")

if __name__ == "__main__":
    main()