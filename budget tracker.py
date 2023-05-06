from tkinter import *
import tkinter.messagebox as tk
import tkinter.ttk as ttk
import pickle as pk
import mysql.connector 

def tablesql(records,field):
    sqlwin=Tk()
    sqlwin.title('Retrived values')
    sqlwin.geometry('1280x900')
    sqlwin.resizable(1, 1)
    d_field=tuple(field)
    n=len(field)
    table=ttk.Treeview(sqlwin, column=d_field,show='headings',height=len(records))
    scrollbar = ttk.Scrollbar(sqlwin,orient ="vertical",command = table.yview)
    scrollbar.pack(side ='right', fill ='y')
    table.configure(yscroll = scrollbar.set)
    for i in range(n):
        table.column(f'#{i+1}',anchor=CENTER)
        table.heading(f'#{i+1}',text=field[i])
    for rec in records:
        table.insert('','end',text='1',values=rec)
    
    table.pack()
    sqlwin.update()
    sqlwin.mainloop()

def mainwin(host_name,usernm,pwd, scrn, theme):
    scrn.destroy()
    root = Tk()
    root.title('Expense Manager')
    root.geometry('1200x550')
    root.resizable(True, True)
    
    entframe=Frame(root, bg=f'{theme}')
    entframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)

    
    def connect():
        mydba=mysql.connector.connect(host=host_name,user=usernm,passwd=pwd)
        mycursor=mydba.cursor()
        cframe=Frame(root, bg=f'{theme}')
        cframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
        cframe.tkraise()
        Label(cframe, text='Enter database name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=100)
        db=Entry(cframe, font=('Times New Roman', 15), width=31, text='Enter database name')
        db.place(x=300, y=100)
        def showdb():
            field=['DATABASES']
            mycursor.execute('SHOW DATABASES')
            record=mycursor.fetchall()
            tablesql(record,field)
        def connected():
            DBNAME=str(db.get())
            mycursor.execute('SHOW DATABASES')
            datb=mycursor.fetchall()
            DBNAME=DBNAME.lower()
            t1=(DBNAME,)
            if t1 in datb:
                mcdb=mysql.connector.connect(host=host_name,user=usernm,passwd=pwd,database=DBNAME)
                tk.showinfo("Sucess", "Connected to Database Sucessfully") 
            else:
                mycursor.execute('CREATE DATABASE '+DBNAME)
                mydba.commit()
                mydba.close()
                mcdb=mysql.connector.connect(host=host_name,user=usernm,passwd=pwd,database=DBNAME)
                tk.showinfo("Success", "Created New and Connected to Database Sucessfully")
            entframe.tkraise()
            def addframe():
                mycursor=mcdb.cursor(buffered=True)
                aframe=Frame(root, bg=f'{theme}')
                aframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
                aframe.tkraise()
    

                Label(aframe, text='Enter table name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=150)
                tben=Entry(aframe, font=('Times New Roman', 15), width=31, text='Enter table name')
                tben.place(x=300, y=150)

                Label(aframe, text='Enter SNo', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=200)
                sno=Entry(aframe, font=('Times New Roman', 15), width=31, text='Enter SNo')
                sno.place(x=300, y=200)

                Label(aframe, text='Enter Type of expense', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=250)
                typ=Entry(aframe, font=('Times New Roman', 15), width=31, text='Enter Type of expense')
                typ.place(x=300, y=250)
 
                Label(aframe, text='Enter Amount Spent', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=300)
                amt=Entry(aframe, font=('Times New Roman', 15), width=31, text='Enter Amount Spent')
                amt.place(x=300, y=300)

                Label(aframe, text='Enter Recipient Name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=350)
                rec=Entry(aframe, font=('Times New Roman', 15), width=31, text='Enter Recipient Name')
                rec.place(x=300, y=350)
    
                Label(aframe, text='Enter Date of Transaction', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=400)
                date=Entry(aframe, font=('Times New Roman', 15), width=31, text='Enter Date of Transaction')
                date.place(x=300, y=400)

                Label(aframe, text='Enter Mode of Transaction', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=450)
                mode=Entry(aframe, font=('Times New Roman', 15), width=31, text='Enter Mode of Transaction')
                mode.place(x=300, y=450)

                def addsql():
                    DBNAME=str(db.get())
                    try:
                        TBNAME=str(tben.get())
                        SNO=str(sno.get())
                        TYPE=str(typ.get())
                        AMOUNT=str(amt.get())
                        RECIPIENT=str(rec.get())
                        DATE=str(date.get())
                        MODE=str(mode.get())
                        mycursor.execute("INSERT INTO "+ TBNAME +" (S_NO,TYPE,AMOUNT,RECIPIENT,DATE_OF_TRANSACTION,MODE_OF_TRANSACTION) VALUES ( "+ SNO +", '"+ TYPE +"' ,"+ AMOUNT+", '"+RECIPIENT+"' , '"+DATE+"' , '"+MODE+"' )")
                        mcdb.commit()
                        tk.showinfo("Sucess", "Values Entered Sucessfully")
                
                    except Exception:
                        tk.showinfo("Error", "Invalid value may be entered")
                    root.update()
                
                    entframe.tkraise()
                def showtable():
                    field=['S_NO','TYPE','AMOUNT','RECIPIENT','DATE_OF_TRANSACTION','MODE_OF_TRANSACTION']
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    mycursor.execute("SELECT * FROM " + TBNAME)
                    
                    record=mycursor.fetchall()
                    tablesql(record,field)
                    
                   
                Button(aframe, text='Add values', command=addsql, font=('Times New Roman', 15), width=20,bg='LightBlue').place(x=300, y=500)
                Button(aframe, text='Back', command=lambda:entframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=20, y=500)
                Button(aframe, text='Show values (Enter table name)', command=showtable, font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=700, y=500)
                root.update()
        
        
            def showframe():
                mycursor=mcdb.cursor(buffered=True)
                sframe=Frame(root, bg=f'{theme}')
                sframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
                sframe.tkraise()
        
                Label(sframe, text='Enter table name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=150)
                tben=Entry(sframe, font=('Times New Roman', 15), width=31, text='Enter table name')
                tben.place(x=800, y=150)
            
                varcharF=('TYPE','RECIPIENT','DATE_OF_TRANSACTION','MODE_OF_TRANSACTION')

                Label(sframe, text='Select fields to be displayed (can select multiple fields)', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=200)
                field=[]
                

                Label(sframe, text='Select fields from which you want to condition ', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=250)
                disfield=[]

                Label(sframe, text='Enter value of the field from which to be displayed', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=300)
                rval=Entry(sframe, font=('Times New Roman', 15), width=31, text='Enter value of the field from which to be displayed')
                rval.place(x=800, y=300)

                Label(sframe, text='Order elements by(Enter Field name)', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=350)
                ofield=[]

                def invoke_b1():
                    if 'S_NO' not in field:
                        field.append('S_NO')
                    
                    b1["state"] = DISABLED
                def invoke_b2():
                    if 'TYPE' not in field:
                        field.append('TYPE')
                    
                    b2["state"] = DISABLED
                def invoke_b3():
                    if 'AMOUNT' not in field:
                        field.append('AMOUNT')
                    
                    b3["state"] = DISABLED
                def invoke_b4():
                    if 'RECIPIENT' not in field:
                        field.append('RECIPIENT')
                    
                    b4["state"] = DISABLED
                def invoke_b5():
                    if 'DATE_OF_TRANSACTION' not in field:
                        field.append('DATE_OF_TRANSACTION')
                    
                    b5["state"] = DISABLED
                def invoke_b6():
                    if 'MODE_OF_TRANSACTION' not in field:
                        field.append('MODE_OF_TRANSACTION')
                    
                    b6["state"] = DISABLED

                
                
                b1=Button(sframe, text='S_NO', command=invoke_b1, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b1.place(x=800, y=200)
                b2=Button(sframe, text='TYPE', command=invoke_b2, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b2.place(x=920, y=200)
                b3=Button(sframe, text='AMOUNT', command=invoke_b3, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b3.place(x=1040, y=200)
                b4=Button(sframe, text='RECIPIENT', command=invoke_b4, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b4.place(x=800, y=220)
                b5=Button(sframe, text='DATE', command=invoke_b5, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b5.place(x=920, y=220)
                b6=Button(sframe, text='MODE', command=invoke_b6, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b6.place(x=1040, y=220)
                print(field)
                
                
                def invoke_b11():
                    if 'S_NO' not in disfield:
                        disfield.append('S_NO')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b12():
                    if 'TYPE' not in disfield:
                        disfield.append('TYPE')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b13():
                    if 'AMOUNT' not in disfield:
                        disfield.append('AMOUNT')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b14():
                    if 'RECIPIENT' not in disfield:
                        disfield.append('RECIPIENT')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b15():
                    if 'DATE_OF_TRANSACTION' not in disfield:
                        disfield.append('DATE_OF_TRANSACTION')
                        
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b16():
                    if 'MODE_OF_TRANSACTION' not in disfield:
                        disfield.append('MODE_OF_TRANSACTION')
                        
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                    
                b11=Button(sframe, text='S_NO', command=invoke_b11, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b11.place(x=800, y=250)
                b12=Button(sframe, text='TYPE', command=invoke_b12, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b12.place(x=920, y=250)
                b13=Button(sframe, text='AMOUNT', command=invoke_b13, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b13.place(x=1040, y=250)
                b14=Button(sframe, text='RECIPIENT', command=invoke_b14, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b14.place(x=800, y=270)
                b15=Button(sframe, text='DATE', command=invoke_b15, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b15.place(x=920, y=270)
                b16=Button(sframe, text='MODE', command=invoke_b16, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b16.place(x=1040, y=270)

                def invoke_b21():
                    if 'S_NO' not in ofield:
                        ofield.append('S_NO')
                    
                    b21["state"] = DISABLED
                    b22["state"] = DISABLED
                    b23["state"] = DISABLED
                    b24["state"] = DISABLED
                    b25["state"] = DISABLED
                    b26["state"] = DISABLED
                def invoke_b22():
                    if 'TYPE' not in ofield:
                        ofield.append('TYPE')
                    
                    b21["state"] = DISABLED
                    b22["state"] = DISABLED
                    b23["state"] = DISABLED
                    b24["state"] = DISABLED
                    b25["state"] = DISABLED
                    b26["state"] = DISABLED
                def invoke_b23():
                    if 'AMOUNT' not in ofield:
                        ofield.append('AMOUNT')
                    
                    b21["state"] = DISABLED
                    b22["state"] = DISABLED
                    b23["state"] = DISABLED
                    b24["state"] = DISABLED
                    b25["state"] = DISABLED
                    b26["state"] = DISABLED
                def invoke_b24():
                    if 'RECIPIENT' not in ofield:
                        ofield.append('RECIPIENT')
                    
                    b21["state"] = DISABLED
                    b22["state"] = DISABLED
                    b23["state"] = DISABLED
                    b24["state"] = DISABLED
                    b25["state"] = DISABLED
                    b26["state"] = DISABLED
                def invoke_b25():
                    if 'DATE_OF_TRANSACTION' not in ofield:
                        ofield.append('DATE_OF_TRANSACTION')
                        
                    b21["state"] = DISABLED
                    b22["state"] = DISABLED
                    b23["state"] = DISABLED
                    b24["state"] = DISABLED
                    b25["state"] = DISABLED
                    b26["state"] = DISABLED
                def invoke_b26():
                    if 'MODE_OF_TRANSACTION' not in ofield:
                        ofield.append('MODE_OF_TRANSACTION')
                        
                    b21["state"] = DISABLED
                    b22["state"] = DISABLED
                    b23["state"] = DISABLED
                    b24["state"] = DISABLED
                    b25["state"] = DISABLED
                    b26["state"] = DISABLED
                    
                b21=Button(sframe, text='S_NO', command=invoke_b21, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b21.place(x=800, y=350)
                b22=Button(sframe, text='TYPE', command=invoke_b22, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b22.place(x=920, y=350)
                b23=Button(sframe, text='AMOUNT', command=invoke_b23, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b23.place(x=1040, y=350)
                b24=Button(sframe, text='RECIPIENT', command=invoke_b24, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b24.place(x=800, y=370)
                b25=Button(sframe, text='DATE', command=invoke_b25, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b25.place(x=920, y=370)
                b26=Button(sframe, text='MODE', command=invoke_b26, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b26.place(x=1040, y=370)
                def enableall():
                    b1["state"] = NORMAL
                    b2["state"] = NORMAL
                    b3["state"] = NORMAL
                    b4["state"] = NORMAL
                    b5["state"] = NORMAL
                    b6["state"] = NORMAL
                    b11["state"] = NORMAL
                    b12["state"] = NORMAL
                    b13["state"] = NORMAL
                    b14["state"] = NORMAL
                    b15["state"] = NORMAL
                    b16["state"] = NORMAL
                    b21["state"] = NORMAL
                    b22["state"] = NORMAL
                    b23["state"] = NORMAL
                    b24["state"] = NORMAL
                    b25["state"] = NORMAL
                    b26["state"] = NORMAL
                    field.clear()
                    disfield.clear()
                    ofield.clear()
                    
                Button(sframe, text='Clear selection', command=enableall, font=('Times New Roman', 10), width=30,bg='LightBlue').place(x=800, y=50)

                
                def showall():
                    field=['S_NO','TYPE','AMOUNT','RECIPIENT','DATE_OF_TRANSACTION','MODE_OF_TRANSACTION']
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    mycursor.execute('SELECT * FROM '+TBNAME)
                    
                    record=mycursor.fetchall()
                    tablesql(record,field)
                def retsql():
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    FNAME=' , '.join(field)
                    ONAME=' , '.join(ofield)
                    cFNAME=' , '.join(disfield)
                    rv=str(rval.get())
                    record=[]
                    if ONAME=='':
                            if cFNAME=='':
                                mycursor.execute('SELECT ' + FNAME+' FROM '+TBNAME)
                                tk.showinfo("Sucess", "Values Retrived Sucessfully")
                                mcdb.commit()
                                record=mycursor.fetchall()
                                
                                
                    
                            elif cFNAME in varcharF:
                                ROWT=str("'"+rv+"'")
                                mycursor.execute('SELECT ' + FNAME+' FROM '+TBNAME+' WHERE ' + cFNAME + ' = ' + ROWT)
                                tk.showinfo("Sucess", "Values Retrived Sucessfully")
                                mcdb.commit()
                                record=mycursor.fetchall()
                                
                                
                    
                            elif cFNAME not in varcharF:
                                ROW=str(rv)
                                mycursor.execute('SELECT ' + FNAME+' FROM '+TBNAME+' WHERE ' + cFNAME + ' = ' + ROW)
                                tk.showinfo("Sucess", "Values Retrived Sucessfully")
                                mcdb.commit()
                                record=mycursor.fetchall()
                               
                                
                    else:
                        
                            if cFNAME=='':
                                mycursor.execute('SELECT ' + FNAME+' FROM '+TBNAME+' ORDER BY '+ ONAME)
                                tk.showinfo("Sucess", "Values Retrived Sucessfully")
                                mcdb.commit()
                                record=mycursor.fetchall()
                                
                    
                            elif cFNAME in varcharF:
                                ROWT=str("'"+rv+"'")
                                mycursor.execute('SELECT ' + FNAME+' FROM '+TBNAME+' WHERE ' + cFNAME + ' = ' + ROWT+' ORDER BY '+ ONAME)
                                tk.showinfo("Sucess", "Values Retrived Sucessfully")
                                mcdb.commit()
                                record=mycursor.fetchall()
                                
                                
                    
                            elif cFNAME not in varcharF:
                                ROW=str(rv)
                                mycursor.execute('SELECT ' + FNAME+' FROM '+TBNAME+' WHERE ' + cFNAME + ' = ' + ROW+' ORDER BY '+ ONAME)
                                tk.showinfo("Sucess", "Values Retrived Sucessfully")
                                mcdb.commit()
                                record=mycursor.fetchall()
                                
                                
                                
                    entframe.tkraise()
                    tablesql(record,field)
                    
                    
                Button(sframe, text='Retrive values', command=retsql, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=300, y=500)
                Button(sframe, text='Show all values', command=showall, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=700, y=500)
                Button(sframe, text='Back', command=lambda:entframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=20, y=500)
        
                root.update()
        
        
            def delframe():
                mycursor=mcdb.cursor(buffered=True)
                tframe=Frame(root, bg=f'{theme}')
                tframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
                tframe.tkraise()

                Label(tframe, text='Enter table name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=150)
                tben=Entry(tframe, font=('Times New Roman', 15), width=31, text='Enter table name')
                tben.place(x=800, y=150)
            
                varcharF=('TYPE','RECIPIENT','DATE_OF_TRANSACTION','MODE_OF_TRANSACTION')

                Label(tframe, text='Enter field name from which value to be deleted(all for whole table)', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=200)
                field=[]
        
                Label(tframe, text='Enter value to be deleted', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=250)
                rval=Entry(tframe, font=('Times New Roman', 15), width=31, text='Enter value to be deleted')
                rval.place(x=800, y=250)

                def invoke_b1():
                    if 'S_NO' not in field:
                        field.append('S_NO')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                def invoke_b2():
                    if 'TYPE' not in field:
                        field.append('TYPE')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                def invoke_b3():
                    if 'AMOUNT' not in field:
                        field.append('AMOUNT')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                def invoke_b4():
                    if 'RECIPIENT' not in field:
                        field.append('RECIPIENT')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                def invoke_b5():
                    if 'DATE_OF_TRANSACTION' not in field:
                        field.append('DATE_OF_TRANSACTION')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                def invoke_b6():
                    if 'MODE_OF_TRANSACTION' not in field:
                        field.append('MODE_OF_TRANSACTION')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                def invoke_all():
                    if 'all' not in field:
                        field.append('all')

                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                

                
                
                b1=Button(tframe, text='S_NO', command=invoke_b1, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b1.place(x=800, y=200)
                b2=Button(tframe, text='TYPE', command=invoke_b2, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b2.place(x=920, y=200)
                b3=Button(tframe, text='AMOUNT', command=invoke_b3, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b3.place(x=1040, y=200)
                b4=Button(tframe, text='RECIPIENT', command=invoke_b4, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b4.place(x=800, y=220)
                b5=Button(tframe, text='DATE', command=invoke_b5, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b5.place(x=920, y=220)
                b6=Button(tframe, text='MODE', command=invoke_b6, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b6.place(x=1040, y=220)
                b7=Button(tframe, text='ALL', command=invoke_all, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b7.place(x=650, y=210)
                
                def enableall():
                    b1["state"] = NORMAL
                    b2["state"] = NORMAL
                    b3["state"] = NORMAL
                    b4["state"] = NORMAL
                    b5["state"] = NORMAL
                    b6["state"] = NORMAL
                    b7["state"] = NORMAL
                    field.clear()
                    
                Button(tframe, text='Clear all selection', command=enableall, font=('Times New Roman', 10), width=30,bg='LightBlue').place(x=800, y=50)
                
                def showall():
                    field=['S_NO','TYPE','AMOUNT','RECIPIENT','DATE_OF_TRANSACTION','MODE_OF_TRANSACTION']
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    mycursor.execute('SELECT * FROM '+TBNAME)
                    mcdb.commit()
                    record=mycursor.fetchall()
                    tablesql(record,field)

                def delsql():
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    FNAME=' , '.join(field)
                    rv=str(rval.get())
            
                    if FNAME=='all':
                            mycursor.execute('DELETE FROM '+TBNAME)
                            tk.showinfo("Sucess", "Values Deleted Sucessfully")
                            mcdb.commit()
                    
                    elif FNAME in varcharF:
                            ROWT=str("'"+rv+"'")
                            mycursor.execute('DELETE FROM '+TBNAME+' WHERE ' + FNAME + ' = ' + ROWT)
                            tk.showinfo("Sucess", "Values Deleted Sucessfully")
                            mcdb.commit()
                    
                    elif FNAME not in varcharF:
                            ROW=str(rv) 
                            mycursor.execute('DELETE FROM '+TBNAME+' WHERE ' + FNAME + ' = ' + ROW)
                            tk.showinfo("Sucess", "Values Deleted Sucessfully")
                            mcdb.commit()
                    record=mycursor.fetchall()
                    tablesql(record,field)
                    entframe.tkraise()
                    tk.showinfo("Sucess", "Values Deleted Sucessfully")
            
                Button(tframe, text='Delete values', command=delsql, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=300, y=500)
                Button(tframe, text='Show all values', command=showall, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=700, y=500)
                Button(tframe, text='Back', command=lambda:entframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=20, y=500)
        
                root.update()

            def updframe():
                mycursor=mcdb.cursor()
                uframe=Frame(root, bg=f'{theme}')
                uframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
                uframe.tkraise()

                Label(uframe, text='Enter table name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=150)
                tben=Entry(uframe, font=('Times New Roman', 15), width=31, text='Enter table name')
                tben.place(x=500, y=150)
    
                Label(uframe, text='Enter field to be changed', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=200)
                field=[]
            
                varcharF=('TYPE','RECIPIENT','DATE_OF_TRANSACTION','MODE_OF_TRANSACTION')
          
                Label(uframe, text='Enter value to be changed', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=250)
                nvalue=Entry(uframe, font=('Times New Roman', 15), width=31, text='Enter value to be changed')
                nvalue.place(x=500, y=250)
            
                Label(uframe, text='Enter field name from which value to be changed', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=300)
                disfield=[]
            
                Label(uframe, text='Enter value of the field from which to be changed', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=350)
                rval=Entry(uframe, font=('Times New Roman', 15), width=31, text='Enter value of the field from which to be changed')
                rval.place(x=500, y=350)
                
                def invoke_b1():
                    if 'S_NO' not in field:
                        field.append('S_NO')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    
                def invoke_b2():
                    if 'TYPE' not in field:
                        field.append('TYPE')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    
                def invoke_b3():
                    if 'AMOUNT' not in field:
                        field.append('AMOUNT')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    
                def invoke_b4():
                    if 'RECIPIENT' not in field:
                        field.append('RECIPIENT')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    b7["state"] = DISABLED
                def invoke_b5():
                    if 'DATE_OF_TRANSACTION' not in field:
                        field.append('DATE_OF_TRANSACTION')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                    
                def invoke_b6():
                    if 'MODE_OF_TRANSACTION' not in field:
                        field.append('MODE_OF_TRANSACTION')
                    
                    b1["state"] = DISABLED
                    b2["state"] = DISABLED
                    b3["state"] = DISABLED
                    b4["state"] = DISABLED
                    b5["state"] = DISABLED
                    b6["state"] = DISABLED
                
                b1=Button(uframe, text='S_NO', command=invoke_b1, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b1.place(x=800, y=200)
                b2=Button(uframe, text='TYPE', command=invoke_b2, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b2.place(x=920, y=200)
                b3=Button(uframe, text='AMOUNT', command=invoke_b3, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b3.place(x=1040, y=200)
                b4=Button(uframe, text='RECIPIENT', command=invoke_b4, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b4.place(x=800, y=220)
                b5=Button(uframe, text='DATE', command=invoke_b5, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b5.place(x=920, y=220)
                b6=Button(uframe, text='MODE', command=invoke_b6, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b6.place(x=1040, y=220)
                
                def invoke_b11():
                    if 'S_NO' not in disfield:
                        disfield.append('S_NO')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b12():
                    if 'TYPE' not in disfield:
                        disfield.append('TYPE')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b13():
                    if 'AMOUNT' not in disfield:
                        disfield.append('AMOUNT')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b14():
                    if 'RECIPIENT' not in disfield:
                        disfield.append('RECIPIENT')
                    
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b15():
                    if 'DATE_OF_TRANSACTION' not in disfield:
                        disfield.append('DATE_OF_TRANSACTION')
                        
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                def invoke_b16():
                    if 'MODE_OF_TRANSACTION' not in disfield:
                        disfield.append('MODE_OF_TRANSACTION')
                        
                    b11["state"] = DISABLED
                    b12["state"] = DISABLED
                    b13["state"] = DISABLED
                    b14["state"] = DISABLED
                    b15["state"] = DISABLED
                    b16["state"] = DISABLED
                    
                b11=Button(uframe, text='S_NO', command=invoke_b11, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b11.place(x=800, y=300)
                b12=Button(uframe, text='TYPE', command=invoke_b12, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b12.place(x=920, y=300)
                b13=Button(uframe, text='AMOUNT', command=invoke_b13, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b13.place(x=1040, y=300)
                b14=Button(uframe, text='RECIPIENT', command=invoke_b14, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b14.place(x=800, y=320)
                b15=Button(uframe, text='DATE', command=invoke_b15, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b15.place(x=920, y=320)
                b16=Button(uframe, text='MODE', command=invoke_b16, font=('Times New Roman', 10), width=15,bg='LightBlue')
                b16.place(x=1040, y=320)

                def enableall():
                    b1["state"] = NORMAL
                    b2["state"] = NORMAL
                    b3["state"] = NORMAL
                    b4["state"] = NORMAL
                    b5["state"] = NORMAL
                    b6["state"] = NORMAL
                    b11["state"] = NORMAL
                    b12["state"] = NORMAL
                    b13["state"] = NORMAL
                    b14["state"] = NORMAL
                    b15["state"] = NORMAL
                    b16["state"] = NORMAL
                    field.clear()
                    disfield.clear()
                    
                Button(uframe, text='Clear all selection', command=enableall, font=('Times New Roman', 10), width=30,bg='LightBlue').place(x=800, y=50)

                

                def showall():
                    field=['S_NO','TYPE','AMOUNT','RECIPIENT','DATE_OF_TRANSACTION','MODE_OF_TRANSACTION']
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    mycursor.execute('SELECT * FROM '+TBNAME)
                    record=mycursor.fetchall()
                    tablesql(record,field)


                def updsql():
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    CHANGEF=' , '.join(field)
                    rv=str(rval.get())
                    FNAME=' , '.join(disfield)
                    nvalt=str(nvalue.get())
            
                    if CHANGEF in varcharF:
                        if FNAME in varcharF:
                            ROWT=str("'"+rv+"'")
                            NVALT=str("'"+nvalt+"'")
                            mycursor.execute('UPDATE '+ TBNAME +' SET '+ CHANGEF +' = '+ NVALT +' WHERE ' + FNAME + ' = ' + ROWT)
                            tk.showinfo("Sucess", "Values Updated Sucessfully")
                            mcdb.commit()
                        else:
                            ROWT=str("'"+rv+"'")
                            NVALT=str(nvalt)
                            mycursor.execute('UPDATE '+ TBNAME +' SET '+ CHANGEF +' = '+ NVALT +' WHERE ' + FNAME + ' = ' + ROWT)
                            tk.showinfo("Sucess", "Values Updated Sucessfully")
                            mcdb.commit()
                            
                            
                    
                    else:
                        if FNAME in varcharF:
                            ROW=str(rv)
                            NVALUE=str("'"+nvalt+"'")
                            mycursor.execute('UPDATE '+ TBNAME +' SET '+ CHANGEF +' = '+ NVALUE +' WHERE ' + FNAME + ' = ' + ROW)
                            tk.showinfo("Sucess", "Values Updated Sucessfully")
                            mcdb.commit()
                        else:
                            ROW=str(rv)
                            NVALUE=str(nvalt)
                            mycursor.execute('UPDATE '+ TBNAME +' SET '+ CHANGEF +' = '+ NVALUE +' WHERE ' + FNAME + ' = ' + ROW)
                            tk.showinfo("Sucess", "Values Updated Sucessfully")
                            mcdb.commit()
                    
                    entframe.tkraise()
                    
            
                Button(uframe, text='Update values', command=updsql, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=300, y=500)
                Button(uframe, text='Show all values', command=showall, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=700, y=500)
                Button(uframe, text='Back', command=lambda:entframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=20, y=500)
        
                root.update()


            def addtbframe():
                mycursor=mcdb.cursor(buffered=True)
                atbframe=Frame(root, bg=f'{theme}')
                atbframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
                atbframe.tkraise()
        
                
                Label(atbframe, text='Enter table name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=150)
                tben=Entry(atbframe, font=('Times New Roman', 15), width=31, text='Enter table name')
                tben.place(x=500, y=150)
                def showtb():
                    field=['TABLES']
                    mycursor.execute('SHOW TABLES')
                    mcdb.commit()
                    record=mycursor.fetchall()
                    tablesql(record,field)
        
                def cretabsql():
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    mycursor.execute('CREATE TABLE ' + TBNAME + ' (S_NO INTEGER PRIMARY KEY ,TYPE VARCHAR(20),AMOUNT FLOAT(12,2) NOT NULL, RECIPIENT VARCHAR(20),DATE_OF_TRANSACTION DATE, MODE_OF_TRANSACTION VARCHAR(15))')
                    tk.showinfo("Sucess", "Table Created Sucessfully")
                    mcdb.commit()                
                    entframe.tkraise()
            
                Button(atbframe, text='CREATE TABLE', command=cretabsql, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=300, y=500)
                Button(atbframe, text='Back', command=lambda:entframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=20, y=500)
                Button(atbframe, text='Show Tables', command=showtb, font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=700, y=500)
        
                root.update()

            def Expenditure():
                mycursor=mcdb.cursor(buffered=True)
                expframe=Frame(root, bg=f'{theme}')
                expframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
                expframe.tkraise()
                
                Label(expframe, text='Enter table name', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=150)
                tben=Entry(expframe, font=('Times New Roman', 15), width=31, text='Enter table name')
                tben.place(x=500, y=150)

                Label(expframe, text='Enter Annual Income', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=200)
                aien=Entry(expframe, font=('Times New Roman', 15), width=31, text='Enter Annual Income')
                aien.place(x=500, y=200)

                def Calc():
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    Label(expframe, text='Total Expenses:', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=400)
                    mycursor.execute('SELECT SUM(AMOUNT) FROM '+TBNAME)
                    mcdb.commit()
                    expsum=mycursor.fetchall()
                    if expsum!=[]:
                        Label(expframe, text=expsum, font=('Times New Roman', 15), bg='White').place(x=500, y=400)
                    else:
                        Label(expframe, text='No value', font=('Times New Roman', 15), bg='White').place(x=500, y=400)
                
                def Calce():
                    TBNAME=str(tben.get())
                    TBNAME=TBNAME.lower()
                    ANIC=aien.get()
                    ANIC=int(ANIC)
                    Label(expframe, text='Savings:', font=('Times New Roman', 15), bg='LightBlue').place(x=50, y=450)
                    mycursor.execute('SELECT SUM(AMOUNT) FROM '+TBNAME)
                    mcdb.commit()
                    expsum=mycursor.fetchall()
                    print(expsum)
                    if expsum!=[]:
                        expsum=expsum[0][0]
                        exp=int(expsum)
                        sav=ANIC-exp
                        Label(expframe, text=sav, font=('Times New Roman', 15), bg='White').place(x=500, y=450)
                    else:
                        Label(expframe, text='No value', font=('Times New Roman', 15), bg='White').place(x=500, y=450)

                Button(expframe, text='GET EXPENDITURE', command=Calc, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=300, y=500)
                Button(expframe, text='GET SAVINGS', command=Calce, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=700, y=500)
                Button(expframe, text='Back', command=lambda:entframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=20, y=500)
                    
            Label(entframe, text='EXPENSE MANAGER', font=('Times New Roman', 15, 'bold'), bg='LightGreen').place(x=475, y=100)
    
            Button(entframe, text='Create new table', command=addtbframe, font=('Times New Roman', 15), width=30,bg='LightBlue',height=3).place(x=100, y=150)
            Button(entframe, text='Calculate Expenditure', command=Expenditure, font=('Times New Roman', 15), width=30,bg='LightBlue',height=3).place(x=750, y=150)
            Button(entframe, text='Add data', command=addframe, font=('Times New Roman', 15), width=30,bg='LightBlue',height=3).place(x=100, y=300)
            Button(entframe, text='Retrive data', command=showframe, font=('Times New Roman', 15), width=30,bg='LightBlue',height=3).place(x=750, y=300)
            Button(entframe, text='Delete data', command=delframe, font=('Times New Roman', 15), width=30,bg='LightBlue',height=3).place(x=100, y=450)
            Button(entframe, text='Update data', command=updframe, font=('Times New Roman', 15), width=30,bg='LightBlue',height=3).place(x=750, y=450)
            Button(entframe, text='EXIT', command=lambda:root.destroy(), font=('Times New Roman', 15), width=15,bg='LightBlue',height=5).place(x=0, y=0)
            
        Button(cframe, text='CONNECT DATABASE', command=connected, font=('Times New Roman', 15), width=20,bg='LightBlue').place(x=20, y=500)
        Button(cframe, text='Show Databases', command=showdb, font=('Times New Roman', 15), width=25,bg='LightBlue').place(x=700, y=500)
        
    r= Button(entframe, text='CONNECT', command=connect, font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=800, y=0)
      
    root.update()
    root.mainloop()

 

def ls():
    tk.showinfo("Login Sucessful", "You are now logged into the system")
    logwin.update()
def lfc():
    tk.showinfo("Failed login", "Confirmation Failed, Please Retry")
    logwin.update()
def lfi():
    tk.showinfo("Login Failed", "Invalid Password")
    logwin.update()
def lfu():
    tk.showinfo("Invalid User", "You are not valid user")
    logwin.update()

def accesswin(theme):
    acwin=Tk()
    acwin.title('DATABASE ACSESS')
    acwin.geometry('800x480')
    acwin.resizable(1, 1)
    acframe=Frame(acwin, bg=f"{theme}")
    acframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
    
    Label(acframe, text='Enter Host name(existing)', font=('Times New Roman', 15), bg='LightBlue').place(x=40, y=100)
    hostn=Entry(acframe, font=('Times New Roman', 15), width=31, text='Enter hostname')
    hostn.place(x=400, y=100)
    
    Label(acframe, text='Enter User name of database(existing)', font=('Times New Roman', 15), bg='LightBlue').place(x=40, y=150)
    usern=Entry(acframe, font=('Times New Roman', 15), width=31, text='Enter username')
    usern.place(x=400, y=150)
    
    Label(acframe, text='Enter password(existing)', font=('Times New Roman', 15), bg='LightBlue').place(x=40, y=200)
    passw=Entry(acframe, font=('Times New Roman', 15), width=31, text='Renter your password ',show='*')
    passw.place(x=400, y=200)

    def connlog():
        host=str(hostn.get())
        user=str(usern.get())
        password=str(passw.get())
        mainwin(host,user,password, acwin, theme)
        
    Button(acframe, text='Connect and Login', command=connlog, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=150, y=300)
    acwin.update()
    acwin.mainloop()
   
def adduser(theme):
    dic={}
    nlogwin=Frame(logwin, bg=f'{theme}')
    nlogwin.place(x=0, y=0, relheight=1.00, relwidth=1.00)
    nlogwin.tkraise()
    Label(nlogwin, text='Enter Username', font=('Times New Roman', 15), bg='LightBlue').place(x=40, y=100)
    entuser=Entry(nlogwin, font=('Times New Roman', 15), width=31, text='Enter Username')
    entuser.place(x=250, y=100)
    
    Label(nlogwin, text='Enter your password', font=('Times New Roman', 15), bg='LightBlue').place(x=40, y=150)
    entpswd=Entry(nlogwin, font=('Times New Roman', 15), width=31, text='Enter your password')
    entpswd.place(x=250, y=150)
    Label(nlogwin, text='Confirm your password', font=('Times New Roman', 15), bg='LightBlue').place(x=40, y=200)
    entcpswd=Entry(nlogwin, font=('Times New Roman', 15), width=31, text='Renter your password to confirm it')
    entcpswd.place(x=250, y=200)
    Button(nlogwin, text='Back', command=lambda:qframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=10, y=300)
    
    def exelog():
        newuser=str(entuser.get())
        while True:
            newpass=str(entpswd.get())
            newpassword=str(entcpswd.get())
            
            if newpassword==newpass and newpassword!='':
                dic[newuser]=newpassword
                with open ('DBlogin.dat','ab') as f:
                    pk.dump(dic,f)
                ls()
                logwin.destroy()
                accesswin(theme)
                                
                break
            
            else:
                lfc()
                break
    Button(nlogwin, text='Confirm and Login', command=exelog, font=('Times New Roman', 15), width=30,bg='LightBlue').place(x=250, y=320)   
    
    

def newframe(theme):
    datframe = Frame(logwin, bg=f'{theme}')
    datframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
    datframe.tkraise() 
    Label(datframe, text='Enter Username', font=('Times New Roman', 15), bg='LightBlue').place(x=80, y=100)
    Label(datframe, text='Enter Password', font=('Times New Roman', 15), bg='LightBlue').place(x=80, y=200)
    entryuser=Entry(datframe, font=('Times New Roman', 15), width=31, text='Enter Username')
    entryuser.place(x=240, y=100)
    entrypass=Entry(datframe, font=('Times New Roman', 15), width=31, text='Enter Password', show='*')
    entrypass.place(x=240, y=200)
    Button(datframe, text='Back', command=lambda:qframe.tkraise(), font=('Times New Roman', 15), width=10,bg='LightBlue').place(x=10, y=300)

    def retriveuser():
        with open ('DBlogin.dat', 'rb') as o:
            dic1={}
            while True:
                try:
                    di=pk.load(o)
                    dic1.update(di)
                except EOFError:
                    break            
        username = str(entryuser.get())
        if username in dic1 :
            password = str(entrypass.get())
            if dic1[username] == password and password!='':
                ls()
                logwin.destroy()
                accesswin(theme)  
            else :
                lfi()       
        else :
            lfu()
    Button(datframe, text='Login', command=retriveuser, font=('Times New Roman', 15), width=5,bg='LightBlue').place(x=350, y=320)



logwin=Tk()
logwin.title('Budget Tracker Login')
logwin.geometry('640x480')
logwin.resizable(1, 1)
logwin.anchor(CENTER)
qframe=Frame(logwin, bg='navy')
qframe.anchor(CENTER)
qframe.place(x=0, y=0, relheight=1.00, relwidth=1.00)
Label(qframe, text='SIGN UP\n if you are a new user', font=('Times New Roman', 15, 'bold'), bg='LightBlue').place(x=200, y=100)
Button(qframe, text='Sign Up', command=lambda: adduser(sel_theme.get()), font=('Times New Roman', 15), width=5,bg='LightBlue').place(x=260, y=200)
Button(qframe, text='Login', command= lambda: newframe(sel_theme.get()), font=('Times New Roman', 15), width=5,bg='LightBlue').place(x=260, y=300)
Label(qframe,text= 'Color Theme', font= ('Calibri', 15, 'bold'), bg='Blue').place(x= 350, y=400)
colors= ['navy', 'blue', 'LightBlue', 'Black', 'Gray', 'Green', 'orange', 'red']
sel_theme= StringVar()
sel_theme.set('navy')
theme= OptionMenu(qframe, sel_theme, 'navy', 'blue', 'LightBlue', 'Black', 'Gray', 'Green', 'orange', 'red' ).place(x= 500, y=400)
Label(qframe, text= '*Theme will be changed inside the application', font=('calibri', 8)).place(x= 380, y=450)
logwin.update()
logwin.mainloop()


    
    
