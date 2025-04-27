#Program Rekap SLIK
#Created by Dofi Kurniawan (T062891)
#import modul
import json
import pandas as pd
import os
import glob 
import datetime
import math
pd.options.mode.chained_assignment = None
#baca data mentah slik
path=os.getcwd()
slik=glob.glob(f'{path}/input/*.txt')
j=1
#load data mentah
for filename in slik:
    with open(filename, encoding='cp1252') as json_file:
        data = json.load(json_file)
    faskred=["kreditPembiayan","garansiYgDiberikan","fasilitasLain"]
    nmr=data['individual']["nomorLaporan"]
    posisi=data['individual']["tanggalPermintaan"]
    col=["Bank","Mata Uang","Fasilitas","Bunga","Maksimum","Baki Debet","Tanggal Mulai","Tanggal Jatuh Tempo","Kolektabilitas","Kondisi"]
    col1=[]
    for i in range(1,25):
        if i<10:
            col1.append(f'tahunBulan0{i}Kol')
        else:
            col1.append(f'tahunBulan{i}Kol')
    #print(col1)
    df_base=pd.DataFrame(columns=col)
    for k in faskred:
        if data['individual']['fasilitas'] [k] != []:
            df_ori=pd.DataFrame(data['individual']['fasilitas'][k])
            #filter kredit pembiayaan
            if k=="kreditPembiayan":
                df=df_ori[["ljkKet","valutaKode","jenisPenggunaanKet","sukuBungaImbalan","plafonAwal","bakiDebet","tanggalMulai","tanggalJatuhTempo","kualitas","kondisiKet"]]    
            #filter garansi bank
            elif k=="garansiYgDiberikan":
                df=df_ori[["ljkKet","kodeValuta","jenisGaransiKet","tanggalWanPrestasi","plafon","nominalBg","tanggalDiterbitkan","tanggalJatuhTempo","kualitas","kondisiKet"]]
            #filter faskred lain
            else :
                df=df_ori[["ljkKet","kodeValuta","jenisFasilitasKet","sukuBungaImbalan","nominalJumlahKwajibanIDR","tunggakan","tanggalMulai","tanggalJatuhTempo","kualitas","kondisiKet"]]
            #df=pd.concat([df1,df2,df3])
            kol=df_ori[col1]
            temp_list=[]
            temp_list_b=[]
            temp_list_c=[]
            for l in range (len(kol)):
                a=pd.to_numeric(kol.iloc[l,:]).max()
                b=pd.to_numeric(kol.iloc[l,:]).idxmax()
                if a==1 or math.isnan(a):
                    temp_list.append("")
                    temp_list_b.append("")
                else:
                    y=df_ori[f'{str(b)[:-3]}Ht'].iloc[0]
                    z=df_ori[str(b)[:-3]].iloc[0]
                    temp_list.append(f'{str(a)} ({z[:-2]}-{z[-2:]}) {str(y)} hari')
                    #print(df_ori[str(b)[:-3]])
                    #z=df_ori[str(b)[:-3]].iloc[0]
                    #temp_list_b.append(f'{z[:-2]}-{z[-2:]}')
            seriess=pd.Series(temp_list)
            #seriess_b=pd.Series(temp_list_b)
            df.columns=col
            df['Ket_Kol_terburuk']=seriess
            #df['Bulan']=seriess_b
            df['NomorLaporan']=nmr
            df['posisi']=posisi
            #reformat tipe data
            for i in ["Maksimum","Baki Debet","Bunga","Kolektabilitas"]:
                df[i]=pd.to_numeric(df[i])
            for i in ["Tanggal Mulai","Tanggal Jatuh Tempo","posisi"]:
                df[i]=pd.to_datetime(df[i])
            df['posisi']=df.posisi+pd.Timedelta(days=-1)
            update=data['individual']["posisiDataTerakhir"]
            df_base=pd.concat([df_base,df])
    df_base['Bunga']=df_base['Bunga']/100
    nama=data['individual']["dataPokokDebitur"][0]["namaDebitur"]
    identitas=data['individual']["dataPokokDebitur"][0]["noIdentitas"]

    #Simpan Ke excel
    #writer=pd.ExcelWriter(f'{path}/hasil/rekap_slik_{nama}_{j}.xlsx',engine='xlsxwriter',date_format='dd/mm/yyyy')
    #workbook=writer.book
    #worksheet=writer.sheets['Sheet1']
    #worksheet.set_column('A:M',20)
    #writer.close()
    #Simpan Ke excel
    #writer=pd.ExcelWriter(f'{path}/hasil/rekap_slik_{nama}_{j}.xlsx',engine='xlsxwriter',date_format='dd/mm/yyyy')
    df_base.to_excel(f'{path}/hasil/rekap_slik_{nama}_{identitas}_{j}.xlsx',index=False)
    j=j+1
print(f'Program Rekap SLIK Versi 0904 \nCreated by Dofi Kurniawan (T062891)')