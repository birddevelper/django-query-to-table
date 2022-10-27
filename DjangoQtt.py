from django.template import Template, Context

import traceback

def generateFromSql(cursor, title, sqltext, footerCols= None, htmlClass="", direction="ltr", font="Tahoma", totalText = "Total", rowIndex = False, headerRowColor ='#eeeeee' ,evenRowColor = '#ffffff', oddRowColor="#ffffff") :
   sumCols=[]
   try :
         if(len(sqltext) < 8 or ("select" not in sqltext.lower())) :
               return ('Not Valid SQL') 

         sql_query = sqltext
         sumCols=footerCols
         # execute sql query and retrieve data from db
         cursor.execute(sql_query)

         # retrieve columns of the data
         desc = cursor.description

         result_as_list = [
            dict(zip([col[0] for col in desc ], row)) for row in cursor.fetchall()
         ]

         columns = [col[0] for col in desc ] #result.keys()
         data = result_as_list
         




         sumOfColumn = None
         if(sumCols != None) :
           sumOfColumn={}

         if(sumCols != None) :
            for c in columns :
               if(c in sumCols):
                  sumOfColumn[c]=0
               else:
                  sumOfColumn[c]="-"

         if(sumCols != None) :
            for d in data :
               for attr, value in dict(d).items() :
                  if(attr in sumCols):
                     sumOfColumn[attr]=sumOfColumn[attr]+int(str(value).replace(",", ""))
         
         totalColumnSet = False
         if(sumCols != None) :
            for col, val in sumOfColumn.items() :
               if(val!="-") :
                  sumOfColumn[col] = format(int(str(val)),",")
               elif (totalColumnSet == False) :
                  sumOfColumn[col] = totalText
                  totalColumnSet = True
         
         # template to generate data from data retrieved from data base

         template= "<center><table dir=\"{{direction}}\"  border=\"1\" class=\"table table-striped {{htmlClass}}\" style=\"width:93%;font-family:'{{font}}'\"> <thead> <tr> <th colspan='{{columns|length|add:'1'}}' style=\"font-family:'{{font}}';font-weight: bold;\"  > {{title}} </th> </tr> <tr style='background-color:{{headerRowColor}}'>{% if rowIndex == True  %} <td align=\"center\"> </td> {% endif %} {% for c in columns %} <th>{{ c }}</th> {% endfor %} </tr> </thead> <tbody> {% for d in data %} <tr style='background-color:{% if forloop.counter0|divisibleby:'2'  %} {{evenRowColor}} {% else %} {{oddRowColor}} {% endif %} '  > {% if rowIndex == True  %}  <td align=\"center\">{{ loop.index }}</td> {% endif %}  {% for attr, value in d.items %} <td align=\"center\">{{ value }}</td> {% endfor %} </tr> {% endfor %} {% if sumOfColumn != None   %} <tr  style='background-color:#eee;font-weight: bold;'> <td></td> {% for a,v in sumOfColumn.items %} <td align=\"center\">{{ v }}</td> {% endfor %} </tr> {% endif %}</tbody> </table></center>"
         
         #print(columns)


         c = Context({
            'title':title,
            'data':data,
            'columns':columns,
            'sumOfColumn':sumOfColumn,
            'direction':direction,
            'font':font,
            'totalText':totalText,
            'rowIndex' : rowIndex,
            'headerRowColor' :headerRowColor ,
            'evenRowColor' : evenRowColor,
            'oddRowColor': oddRowColor,
            'htmlClass' : htmlClass
         })
         #return render_template_string(template,title=title,data=data,columns=columns,sumOfColumn=sumOfColumn,direction=direction,font=font,totalText=totalText, rowIndex = rowIndex, headerRowColor =headerRowColor ,evenRowColor = evenRowColor, oddRowColor= oddRowColor )
         return Template(template).render(c)
   except BaseException as e :
          print(traceback.format_exc())
          return ("Error :" + str(e))   
