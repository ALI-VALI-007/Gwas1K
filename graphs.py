'''
I need 2 primary functions
1. for making the graph
2. for getting the info from the dbs

for 2, we are gonna need to pull from the gwas db, then take the list of rsids to put into the alfa db and get the freqs
This would then plug into the graph functions

for the graph funcs we need one to process the freqs given (as in properly format them and get numbers, a list with [pop,freq] would be good)
after we call that we can just make the graphs with mathplotlib

'''
import sqlite3
import matplotlib.pyplot as plt
import pathlib


def getGwas(disease):
    conn=sqlite3.connect('genome.db')
    cursor=conn.cursor()
    query=f'SELECT snps FROM GWAS WHERE "DISEASE/TRAIT" LIKE "%{disease}%"'
    cursor.execute(query)
    result=cursor.fetchall()
    conn.close()
    return result

def getAlfa(snp):
    #print(snp)
    conn=sqlite3.connect('genome.db')
    cursor=conn.cursor()
    query=f'SELECT eur, afo, eas, afa, lac, len, oas, sas, otr, afr, asn, tot FROM ALFA WHERE id="{snp}"'
    cursor.execute(query)
    result=cursor.fetchall()
    conn.close()
    return result

def fstPass(fst,baseline,greater):
    if greater and fst>baseline:
        return True
    elif not greater and fst<baseline:
        return True
    return False

def processAlfa(ratios):
    res=[]
    total=ratios[-1].split(':')
    n1=float(total[0].replace(',',''))
    p1=float(total[1].replace(',',''))/n1
    fstPassed=False
    for i in range(len(ratios)-1):
        #print(ratio)
        ratio=ratios[i]
        temp=ratio.split(':')
        n2=float(temp[0].replace(',',''))
        p2=float(temp[1].replace(',',''))
        #print(x)
        if n2>0:
            p2=p2/n2
            hw=p1*(1-p1)/n1+p2*(1-p2)/n2
            hb=p1*(1-p2)+p2*(1-p1)
            fst=0
            if hb>0:
                fst=hw/hb
                if fstPass(fst,0.1,True):
                    fstPassed=True
            res.append(p2/n2)
        else:
            res.append(0)
    if fstPassed:
        return res
    return None

def makeBarGraph(freqs,snp):
    pops=['EUR','AFO','EAS','AFA','LAC','LEN','OAS','SAS','OTR','AFR','ASN']
    #print(freqs)
    plt.bar(pops,freqs,color='skyblue')
    plt.xlabel('Populations')
    plt.ylabel('Frequencies')
    plt.title(snp)
    plt.savefig('graphs/'+'BarGraph-'+snp)

def fileCheck(rsid):
    filePath=pathlib.Path('graphs/BarGraph-'+str(rsid)+'.png')
    return filePath.exists()

def isMakeGraph(freqs):
    for freq in freqs:
        if freq != 0:
            return True
    return False

def userInput(disease):
    print("Searching "+disease)
    snpList=getGwas(disease)
    graphsMade=[]
    for snpTuple in snpList:
        snp=snpTuple[0]
        if " " in snp:
            print("Snp name invalid")
        elif not fileCheck(snp):
            freqListTuple=getAlfa(snp)
            if freqListTuple != None and len(freqListTuple)>0:
                freqListStr=freqListTuple[0]
                freqList=processAlfa( freqListStr )
                if freqList != None and isMakeGraph(freqList):
                    makeBarGraph(freqList,snp)
                    graphsMade.append(snp)
                    print(snp+" Graph made")
        else:
            graphsMade.append(snp)
            print("File Found: "+snp)
    print("All graphs made")
    return graphsMade
    #we return the snplist so this way we can get the pngs on the frontend

#Test to see if it works properly pre frontend
'''
disease=input("enter disease:")
userInput(disease)
print("Done")
'''
