import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd

class Dataframes:
  def __init__(self, contextual_classes, conceptual_classes, logical_classes, contextual_properties, conceptual_properties, logical_properties): 
      self.classes = contextual_classes
      self.properties = contextual_properties

def urn_in_model(urn, model):
  return model in urn

def import_xmi(directory):
  print('Searching for .xmi files in directory:', directory)

  for path in Path(directory).rglob('*.xmi'):
    print('  *.xmi file found: ', path)

    print('Creating tree...')   
    tree = ET.parse(path)
    print('Getting the root...') 
    root = tree.getroot()

    number_uml_class = 0
    number_uml_association = 0
    number_uml_property = 0
    
    number_element = 0
    number_class_contextual = 0
    number_class_conceptual = 0
    number_class_logical = 0
    number_attribute = 0
    number_attribute_contextual = 0
    number_attribute_conceptual = 0
    number_attribute_logical = 0

    df_class_cols = ["urn", "name", "definition", "package", "parent_class"]
    df_property_cols = ["urn", "name", "definition", "parent", "type"]
    contextual_class_rows = []
    contextual_property_rows = []
    conceptual_class_rows = []
    conceptual_property_rows = []
    logical_class_rows = []
    logical_property_rows = []

    print('Exploring children...') 
    for child in root:
      if child.tag =='{http://schema.omg.org/spec/XMI/2.1}Extension':
        for sub_child in child:
          if sub_child.tag == 'elements':
            for element in sub_child:
              if element.tag == 'element': #Encuentra los <element> dentro de <elements>
                
                id_ref = element.attrib.get("{http://schema.omg.org/spec/XMI/2.1}idref")
                element_type = element.attrib.get("{http://schema.omg.org/spec/XMI/2.1}type")
                element_name = element.attrib.get("name")
                element_definition = '' 
                element_urn = ''
                element_package_name = ''
                element_synonyms = ''
                element_definition_source = ''
                element_abbreviation = ''
                element_parent_class = ''
                
                attribute_name = ''
                attribute_definition = ''
                attribute_urn = ''
                attribute_synonyms = ''
                attribute_definition_source = ''
                attribute_abbreviation = ''
                attribute_type = ''


                for sub_element in element:
                  if sub_element.tag == 'properties':
                    element_definition = sub_element.attrib.get("documentation")    
                  elif sub_element.tag == 'extendedProperties':
                    element_package_name = sub_element.attrib.get("package_name")
                  elif sub_element.tag == 'tags':
                    for tag in sub_element:
                      if tag.tag == 'tag':
                        if tag.attrib.get("name") == 'URN':
                          element_urn = tag.attrib.get("value")
                        elif tag.attrib.get("name") == 'Definition:Synonyms':
                          element_synonyms = tag.attrib.get("value")
                        elif tag.attrib.get("name") == 'Definition:Source':
                          element_definition_source = tag.attrib.get("value") #process
                        elif tag.attrib.get("name") == 'Definition:Abbreviation':
                          element_abbreviation = tag.attrib.get("value") 
                  
                  elif sub_element.tag == 'attributes':
                    for attribute in sub_element:
                      if attribute.tag == 'attribute':
                        attribute_name = attribute.attrib.get("name")
                        for sub_attribute in attribute:
                          if sub_attribute.tag == 'documentation':
                            attribute_definition = sub_attribute.attrib.get("value")
                          elif sub_attribute.tag == 'properties':
                            attribute_type = sub_attribute.attrib.get("type")
                          elif sub_attribute.tag == 'tags':
                            for tag in sub_attribute:
                              if tag.tag == 'tag':
                                if tag.attrib.get("name") == 'URN':
                                  attribute_urn = tag.attrib.get("value")
                                elif tag.attrib.get("name") == 'Definition:Synonyms':
                                  attribute_synonyms = tag.attrib.get("value")
                                elif tag.attrib.get("name") == 'Definition:Source':
                                  attribute_definition_source = tag.attrib.get("value") #process
                                elif tag.attrib.get("name") == 'Definition:Abbreviation':
                                  attribute_abbreviation = tag.attrib.get("value") 
                      if attribute_urn != '':
                        number_attribute+=1  
                        if urn_in_model(attribute_urn, "ContextualModel"):
                          number_attribute_contextual+=1 
                          contextual_property_rows.append({"urn": attribute_urn, "name": attribute_name, "definition": attribute_definition, "parent": element_name, "type": attribute_type})
                        elif urn_in_model(attribute_urn, "ConceptualModel"):
                          number_attribute_conceptual+=1 
                          conceptual_property_rows.append({"urn": attribute_urn, "name": attribute_name, "definition": attribute_definition, "parent": element_name, "type": attribute_type})
                        elif urn_in_model(attribute_urn, "LogicalModel"):
                          number_attribute_logical+=1 
                          logical_property_rows.append({"urn": attribute_urn, "name": attribute_name, "definition": attribute_definition, "parent": element_name, "type": attribute_type})
                      
                  elif sub_element.tag == 'links':
                    for link in sub_element:
                      if link.tag == 'Generalization':     
                        element_parent_class = link.attrib.get("{http://schema.omg.org/spec/XMI/2.1}id")


                #print('['+element_package_name+']', element_name, element_urn)
                if element_urn != '':
                        number_element+=1  
                        if urn_in_model(element_urn, "ContextualModel"):
                          number_class_contextual+=1 
                          contextual_class_rows.append({"urn": element_urn, "name": element_name, "definition": element_definition, "package": element_package_name, "parent_class": element_parent_class})
                        elif urn_in_model(element_urn, "ConceptualModel"):
                          number_class_conceptual+=1 
                          conceptual_class_rows.append({"urn": element_urn, "name": element_name, "definition": element_definition, "package": element_package_name, "parent_class": element_parent_class})
                        elif urn_in_model(element_urn, "LogicalModel"):
                          number_class_logical+=1 
                          logical_class_rows.append({"urn": element_urn, "name": element_name, "definition": element_definition, "package": element_package_name, "parent_class": element_parent_class})

          elif sub_child.tag == 'connectors':
            for connector in sub_child:
              if connector.tag == 'connector': #Encuentra los <connector> dentro de <connectors>
                attribute_name = ''
                attribute_definition = ''
                attribute_urn = ''
                element_name = ''
                attribute_type = ''
                
                for sub_connector in connector:
                  if sub_connector.tag == 'source':
                    for element in sub_connector:
                      if element.tag  == 'model':
                        attribute_type = element.attrib.get("name")  
                      elif element.tag  == 'role':
                        attribute_name = element.attrib.get("name")
                      elif element.tag == 'documentation':
                        attribute_definition = element.attrib.get("value")
                      elif element.tag == 'tags':
                            for tag in element:
                              if tag.tag == 'tag':
                                if tag.attrib.get("name") == 'URN':
                                  attribute_urn = tag.attrib.get("value")
                  elif sub_connector.tag == 'target':
                    for element in sub_connector:
                      if element.tag  == 'model':
                        element_name = element.attrib.get("name")
                if attribute_urn == '':
                  for sub_connector in connector:
                    if sub_connector.tag == 'target':
                      for element in sub_connector:
                        if element.tag  == 'model':
                          attribute_type = element.attrib.get("name")  
                        elif element.tag  == 'role':
                          attribute_name = element.attrib.get("name")
                        elif element.tag == 'documentation':
                          attribute_definition = element.attrib.get("value")
                        elif element.tag == 'tags':
                              for tag in element:
                                if tag.tag == 'tag':
                                  if tag.attrib.get("name") == 'URN':
                                    attribute_urn = tag.attrib.get("value")
                    elif sub_connector.tag == 'source':
                      for element in sub_connector:
                        if element.tag  == 'model':
                          element_name = element.attrib.get("name")

                if attribute_urn != '':
                        number_attribute+=1  
                        if urn_in_model(attribute_urn, "ContextualModel"):
                          number_attribute_contextual+=1 
                          contextual_property_rows.append({"urn": attribute_urn, "name": attribute_name, "definition": attribute_definition, "parent": element_name, "type": attribute_type})
                        elif urn_in_model(attribute_urn, "ConceptualModel"):
                          number_attribute_conceptual+=1 
                          conceptual_property_rows.append({"urn": attribute_urn, "name": attribute_name, "definition": attribute_definition, "parent": element_name, "type": attribute_type})
                        elif urn_in_model(attribute_urn, "LogicalModel"):
                          number_attribute_logical+=1 
                          logical_property_rows.append({"urn": attribute_urn, "name": attribute_name, "definition": attribute_definition, "parent": element_name, "type": attribute_type})
                  
            
  #TODO: procesar connectors como atributos. separar main de supplements. volcar todo a diccionarios/dataframes y excel.


  print('Number of element:', number_element)
  print('Number of element in Contextual:', number_class_conceptual)
  print('Number of element in Conceptual:', number_class_logical)
  print('Number of element in Logical:', number_class_contextual)
  print('Number of attribute:', number_attribute)
  print('Number of attribute in Contextual:', number_attribute_contextual)
  print('Number of attribute in Conceptual:', number_attribute_conceptual)
  print('Number of attribute in Logical:', number_attribute_logical)
        
    
  
  out_contextual_class_df = pd.DataFrame(contextual_class_rows, columns = df_class_cols)
  out_conceptual_class_df = pd.DataFrame(conceptual_class_rows, columns = df_class_cols)
  out_logical_class_df = pd.DataFrame(logical_class_rows, columns = df_class_cols)
  out_property_contextual_df = pd.DataFrame(contextual_property_rows, columns = df_property_cols)      
  out_property_conceptual_df = pd.DataFrame(conceptual_property_rows, columns = df_property_cols) 
  out_property_logical_df = pd.DataFrame(logical_property_rows, columns = df_property_cols) 
  print('  *No more files to process')

  with pd.ExcelWriter('data/xlsx/'+'AIRM 1.0.0.xlsx', engine='xlsxwriter') as writer:  
      out_contextual_class_df.to_excel(writer, sheet_name='Contextual Classes')
      out_conceptual_class_df.to_excel(writer, sheet_name='Conceptual Classes')
      out_logical_class_df.to_excel(writer, sheet_name='Logical Classes')

      out_property_contextual_df.to_excel(writer, sheet_name='Contextual Properties')
      out_property_conceptual_df.to_excel(writer, sheet_name='Conceptual Properties')
      out_property_logical_df.to_excel(writer, sheet_name='Logical Properties')
  
  return Dataframes(out_contextual_class_df, out_conceptual_class_df, out_logical_class_df,  out_property_contextual_df, out_property_conceptual_df, out_property_logical_df)

def find_urn(urn, dataframes):
  
  if "@" in urn:
    print("@ found")
    filter = dataframes.properties["urn"]==urn
    dataframes.properties.sort_values("urn", inplace = True)
    dataframes.properties.where(filter, inplace = True) 
    return dataframes.properties.dropna(how='all')
  else:
    print("@ not found")
    filter = dataframes.classes["urn"]==urn
    dataframes.classes.sort_values("urn", inplace = True) 
    dataframes.classes.where(filter, inplace = True) 
    return dataframes.classes.dropna(how='all')
  
def old_load_and_find_urn(urn):
  dfc = pd.read_excel (r'data/xlsx/AIRM 1.0.0.xlsx', sheet_name='Classes')
  dfp = pd.read_excel (r'data/xlsx/AIRM 1.0.0.xlsx', sheet_name='Properties')
  dataframes = Dataframes(dfc, dfp)
  if "@" in urn:
    print("@ found")
    filter = dataframes.properties["urn"]==urn
    dataframes.properties.sort_values("urn", inplace = True)
    dataframes.properties.where(filter, inplace = True) 
    result = dataframes.properties.dropna(how='all')
    name = result["name"].iloc[0]
    return name
  else: 
    print("@ not found")
    filter = dataframes.classes["urn"]==urn
    dataframes.classes.sort_values("urn", inplace = True) 
    dataframes.classes.where(filter, inplace = True) 
    result = dataframes.classes.dropna(how='all')
    name = result["name"].iloc[0]
    return name

def valid_urn(urn): #TO DO: adapt regex to urn grammar
  import re
  regex = re.compile(
          r'^(?:http|ftp)s?://' # http:// or https://
          r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
          r'localhost|' #localhost...
          r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
          r'(?::\d+)?' # optional port
          r'(?:/?|[/?]\S+)$', re.IGNORECASE)

  return re.match(regex, urn)

def load_and_find_urn(urn):
  print(urn)
  entry = {
      "name": "invalid urn",
      "definition": "invalid urn"
    }
  if "urn:" in urn:#if valid_urn(urn):
    if "@" in urn:
      dataframe = pd.read_excel (r'data/xlsx/AIRM 1.0.0.xlsx', sheet_name='Properties')
    else:
      dataframe = pd.read_excel (r'data/xlsx/AIRM 1.0.0.xlsx', sheet_name='Classes')

    filter = dataframe["urn"]==urn
    dataframe.sort_values("urn", inplace = True)
    dataframe.where(filter, inplace = True) 
    result = dataframe.dropna(how='all')
    print(result)
    if result.empty:
      entry = {
        "name": "not found",
        "definition": "not found"
      }
    else:
      entry = {
        "name": result["name"].iloc[0],
        "definition": result["definition"].iloc[0]
      }
  
  return entry