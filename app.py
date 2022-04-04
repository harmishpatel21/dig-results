from components.pipeline import main

if __name__ == '__main__':
    main()

   
        
#         export_combined_df = st.checkbox('Export Combined Dataframe')
#         if export_combined_df:
#             combined_df = pd.concat([dent_df, metalloss_df], ignore_index=True)
#             st.write(combined_df)
#             # print(len(combined_df))
#             dp.export_data(combined_df, 'Calculated Combined dataframe')
#     except:
#         st.write('No data to show')