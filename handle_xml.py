import xml.etree.ElementTree as ET
from barcode import EAN13 
from barcode.writer import ImageWriter
import json


dataDict = {}

def parse_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    
    
    print("---------------infNFe NODES-----------------")
    infNFe_attrib = root[0][0].attrib
    ch_acesso = infNFe_attrib['Id']
    
    ide_node = root[0][0][0]
    emit_node = root[0][0][1]
    child_enderEmit_node = emit_node[2]
    dest_node = root[0][0][2]
    child_enderDest_node = dest_node[2]
    
    
    modFrete_node = root[0][0][8][0]
    transp_node = root[0][0][8][1]
    vol_node = root[0][0][8][2]
    
    protNFe_node = root[1][0]
    
    """ DET (Detalhamento Prod) """
    
    
    """ infNFe Nodes Dicts """
    ide_Dict = {}
    emit_Dict = {}
    child_enderEmit_Dict = {}
    dest_Dict = {}
    child_enderDest_Dict = {}
    
    transp_Dict = {}
    vol_Dict = {}
    
    protNFe_Dict = {}
    det_Dict = {}
    prod_Dict = {}
    
    """ FOR LOOPS """
    
    """infNFe_Attrib"""
    item = ch_acesso
    ch = item.replace('NFe','')
    dataDict['infNFe_Attrib'] = ch
    
    """ IDE """
    for item in ide_node:
        tag = str(item.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        ide_Dict[key] = item.text
    dataDict['ide'] = ide_Dict
    
    """ EMIT """
    
    for item in emit_node:
        tag = str(item.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        if key != "enderEmit":
            emit_Dict[key] = item.text        
    dataDict['emit'] = emit_Dict
    
    """ Child enderEmit """
    
    for child in child_enderEmit_node:
        tag = str(child.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        child_enderEmit_Dict[key] = child.text
    dataDict['enderEmit'] = child_enderEmit_Dict
    
    """ dest """
    
    for item in dest_node:
        tag = str(item.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        if key != "enderDest":
            dest_Dict[key] = item.text        
    dataDict['dest'] = dest_Dict
    
    """ Child enderDest """
    
    for child in child_enderDest_node:
        tag = str(child.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        child_enderDest_Dict[key] = child.text
    dataDict['enderDest'] = child_enderDest_Dict
    
    
    
    """ modFrete """
    
    item = modFrete_node.text
    dataDict['modFrete'] = item
    
    """ transporta """
    
    for item in transp_node:
        tag = str(item.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        transp_Dict[key] = item.text
        dataDict['transporta'] = transp_Dict
    
    """ vol """
    
    for item in vol_node:
        tag = str(item.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        vol_Dict[key] = item.text
        dataDict['vol'] = vol_Dict
    
    
    """ infProt """
    
    for item in protNFe_node:
        tag = str(item.tag)
        key = tag.replace("{http://www.portalfiscal.inf.br/nfe}", "")
        protNFe_Dict[key] = item.text
        dataDict['infProt'] = protNFe_Dict
    
    """ Prod """
    
    url = '{http://www.portalfiscal.inf.br/nfe}'
    for det in root.iter(url+'det'):
        det_tag = det.attrib
        print("DET_TAG: "+str(det_tag))
        for key_prod, value_prod in det_tag.items():
            print("KEY, VALUE: "+ key_prod, value_prod)
            for item_prod in det.findall(url+'prod'):
                print("ITEM_PROD: "+ str(item_Dict))
                for child_prod in item_prod:
                    print("CHILD: "+str(child_prod.text))
                    print(child_prod.tag.replace(url, '') + ' ' +child_prod.text)
                    prod_Dict[f'{item_prod.tag}'.replace(url, '')]
                    item_Dict[f'{child_prod.tag}'.replace(url, '')] = child_prod.text
                det_Dict[f'{key_prod} {value_prod}'] = prod_Dict
        print("DET_DICT"+ str(det_Dict))
        
        number = str(protNFe_Dict['chNFe'])
        if len(number) <= 48:
            number = number.zfill(48)
        my_code = EAN13(number, writer=ImageWriter()) 
        my_code.save("core/static/images/bar_code")
        dataDict['BarCode'] = number
    
    return dataDict
    