import traceback
import warnings
from django.template import Template, Context
from django.db import connection
import logging

logger = logging.getLogger(__name__)

def _validate_sql(sqltext):
   """Validate the SQL query."""
   if len(sqltext) < 8 or ("select" not in sqltext.lower()):
      return False
   return True

def _execute_query(cursor, sqltext):
   """Execute the SQL query and fetch data."""
   cursor.execute(sqltext)
   desc = cursor.description
   result_as_list = [
      dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
   ]
   columns = [col[0] for col in desc]
   return columns, result_as_list

def _calculate_sums(data, columns, footerCols, totalText):
   """Calculate sum for specified columns."""
   sumOfColumn = {col: 0 if col in footerCols else "-" for col in columns}
   
   for d in data:
      for attr, value in d.items():
            if attr in footerCols:
               sumOfColumn[attr] += float(str(value).replace(",", ""))

   totalColumnSet = False
   for col in sumOfColumn:
      if sumOfColumn[col] != "-":
            sumOfColumn[col] = format(float(str(sumOfColumn[col])), ",")
      elif not totalColumnSet:
            sumOfColumn[col] = totalText
            totalColumnSet = True

   return sumOfColumn

def _render_template(context):
   """Render the HTML table template."""
   template = (
      "<center><table dir=\"{{direction}}\"  border=\"1\" class=\"table table-striped {{htmlClass}}\" "
      "style=\"width:93%;font-family:'{{font}}'\">"
      " <thead> <tr> <th colspan='{{columns|length|add:'1'}}' style=\"font-family:'{{font}}';font-weight: bold;\"  > {{title}} </th> </tr>"
      " <tr style='background-color:{{headerRowColor}}'>{% if rowIndex %} <th align=\"center\"> # </th> {% endif %} {% for c in columns %} <th>{{ c }}</th> {% endfor %} </tr> </thead>"
      " <tbody> {% for d in data %} <tr style='background-color:{% if forloop.counter0|divisibleby:'2'  %} {{evenRowColor}} {% else %} {{oddRowColor}} {% endif %} '  >"
      " {% if rowIndex %}  <td align=\"center\">{{ forloop.counter }}</td> {% endif %}  {% for attr, value in d.items %} <td align=\"center\">{{ value }}</td> {% endfor %} </tr> {% endfor %} "
      " {% if sumOfColumn %} <tr  style='background-color:#eee;font-weight: bold;'> <td></td> {% for a,v in sumOfColumn.items %} <td align=\"center\">{{ v }}</td> {% endfor %} </tr> {% endif %}</tbody> </table></center>"
   )

   return Template(template).render(Context(context))

def _generate_report(cursor, title, sqltext, footerCols, htmlClass, direction, font, totalText, rowIndex, headerRowColor, evenRowColor, oddRowColor):
   """Internal method to generate the SQL report."""
   columns, data = _execute_query(cursor, sqltext)

   sumOfColumn = None
   if footerCols:
      sumOfColumn = _calculate_sums(data, columns, footerCols, totalText)

   context = {
      'title': title,
      'data': data,
      'columns': columns,
      'sumOfColumn': sumOfColumn,
      'direction': direction,
      'font': font,
      'totalText': totalText,
      'rowIndex': rowIndex,
      'headerRowColor': headerRowColor,
      'evenRowColor': evenRowColor,
      'oddRowColor': oddRowColor,
      'htmlClass': htmlClass
   }

   return _render_template(context)

def generate_from_sql(title, sqltext, footerCols=None, htmlClass="", direction="ltr", font="Tahoma", totalText="Total", rowIndex=False, headerRowColor='#eeeeee', evenRowColor='#ffffff', oddRowColor="#ffffff"):
   """Generate the SQL report with an internally created cursor."""
   try:
      if not _validate_sql(sqltext):
            return 'Not Valid SQL'

      with connection.cursor() as cursor:
            return _generate_report(cursor, title, sqltext, footerCols, htmlClass, direction, font, totalText, rowIndex, headerRowColor, evenRowColor, oddRowColor)
   except Exception as e:
      logger.error(traceback.format_exc())
      return f"Error: {str(e)}"

def generateFromSql(cursor, title, sqltext, footerCols=None, htmlClass="", direction="ltr", font="Tahoma", totalText="Total", rowIndex=False, headerRowColor='#eeeeee', evenRowColor='#ffffff', oddRowColor="#ffffff"):
   """Generate the SQL report with a provided cursor."""
   warnings.warn("generateFromSql is deprecated and will be removed in a future release. Use generate_from_sql instead.", DeprecationWarning)
   try:
      if not _validate_sql(sqltext):
            return 'Not Valid SQL'

      return _generate_report(cursor, title, sqltext, footerCols, htmlClass, direction, font, totalText, rowIndex, headerRowColor, evenRowColor, oddRowColor)
   except Exception as e:
      logger.error(traceback.format_exc())
      return f"Error: {str(e)}"