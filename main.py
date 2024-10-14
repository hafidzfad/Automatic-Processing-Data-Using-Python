def mainProcess():
    
    df1 = pd.read_excel(fileA)  # FILE TRANSAKSI BULANAN
    df2 = pd.read_excel(fileB)  # FILE ADMIN TRANSAKSI
    df3 = pd.read_excel(fileC)  # FILE AKHIR / INPUT

# MENDAPAT NILAI PROPOSE

    df1.rename(columns={'agent_id':'AGENT_ID'}, inplace=True)
    df1.rename(columns={'description':'Nama Produk'}, inplace=True)


    df1['Nama Produk']=df1['Nama Produk'].str.lower()
    df2['Nama Produk']=df2['Nama Produk'].str.lower()
    df4 = pd.merge(df1, df2[['Nama Produk', 'Nilai Propose']], on='Nama Produk', how='left')


    # MENGUBAH MENJADI FIX INPUT AGENT

    df4 = df4.groupby(by="AGENT_ID").sum()[["Nilai Propose"]]
    df4["Korgen_40%"] = (df4["Nilai Propose"]) * 0.4
    df4["Agent_60%"] = (df4["Nilai Propose"]) * 0.6
    df4["Korlap_10%"] = (df4["Agent_60%"]) * 0.1
    df4["Agent_Recieved"] = (df4["Agent_60%"]) - (df4["Korlap_10%"])
    df4["Fix_Input_Agent"] = np.floor(df4["Agent_Recieved"])
    df4.reset_index(inplace=True)

    # MENGINPUT KE FILE INPUT 

    df5 = pd.merge(df3, df4[['AGENT_ID','Fix_Input_Agent']], on='AGENT_ID', how='left')
    df6 = df5['Fix_Input_Agent'].fillna(value = 0)

    df3["TRANSFER_VALUE"] = df6
