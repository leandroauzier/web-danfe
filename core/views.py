from jinja2 import FileSystemLoader, Environment
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from handle_xml import parse_xml
from os.path import exists
from datetime import datetime
import pdfkit
import pytz
import os


def Index(request):
    return render(request, "index.html")

                  
def Handle_Form(request):
    if request.method == "POST":
        
        # Save the uploaded file in tmp first
        data = request.FILES["arquivoXml"]
        tmp_save = 'media/tmp/arquivoxml.xml'
        if exists(tmp_save):
            os.remove(tmp_save)
        path = default_storage.save('tmp/arquivoxml.xml', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        
        # Get the file and parse it
        parsed_data = parse_xml(tmp_save)
        
        # Call Save function to pdf
        print(parsed_data)
        BuildNF(parsed_data)
        SavePDF()
    return render(request, "output/output.html")

def BuildNF(parsed_data):
    loader = FileSystemLoader('core/templates')
    env = Environment(loader=loader)
    template = env.get_template('nfe.html')
    
    file = open('core/templates/output/output.html', 'w', encoding="utf-8")
    
    """ Some data adjustments """
    
    """FORMAT CH"""
    ch = parsed_data['infNFe_Attrib']
    ch_acesso = '{} {} {} {} {} {} {} {} {} {} {}'.format(ch[:4],ch[4:9],ch[9:13],ch[13:17],ch[17:21],ch[21:25],ch[25:29],ch[29:33],ch[33:37],ch[37:41],ch[41:45])
    
    """FORMAT NF"""
    nNF = parsed_data['ide']['nNF']
    if len(nNF) < 9:
        nNF = nNF.zfill(9)
        num_NF = '{}.{}.{}'.format(nNF[:3],nNF[3:6],nNF[6:9])
        
    """FORMAT série"""
    serie = parsed_data['ide']['serie']
    if len(serie) < 3:
        num_serie = serie.zfill(3)
    
    """ DATA EMISSAO """
    _dhEmi = parsed_data['ide']['dhEmi']
    dia = _dhEmi[8:10]
    mes = _dhEmi[5:7]
    ano = _dhEmi[0:4]
    dateEmi = f"{dia}/{mes}/{ano}"
    
    """ CPF/CNPJ """
    cnpj_emit = Format_CPF_CNPJ(parsed_data['emit']['CNPJ'])
    cnpj_dest = Format_CPF_CNPJ(parsed_data['dest']['CNPJ'])
    cnpj_tranp = Format_CPF_CNPJ(parsed_data['transporta']['CNPJ'])
    
    """ CEP """
    cep_dest = Format_CEP(parsed_data['enderDest']['CEP'])
    
    
    """ Transporta """
    transporta_nome = parsed_data['transporta']['xNome']
    
    """Peso replacement"""
    """Liquido"""
    pesoL = String_replacement(parsed_data['vol']['pesoL'],'.',',')
    """Bruto"""
    pesoB = String_replacement(parsed_data['vol']['pesoB'],'.',',')
    
    
    
    """ Data rendering """
    render = template.render(
        ch_acesso=ch_acesso,
        
        nNF=num_NF, cUF=parsed_data['ide']['cUF'],
        serie=num_serie, natOp=parsed_data['ide']['natOp'],
        dhEmi=dateEmi,tpNF=parsed_data['ide']['tpNF'],
        
        xNome_emit=parsed_data['emit']['xNome'],xLgr_emit=parsed_data['enderEmit']['xLgr'],nro_emit=parsed_data['enderEmit']['nro'],
        xCpl_emit=parsed_data['enderEmit']['xCpl'],xBairro_emit=parsed_data['enderEmit']['xBairro'],CEP_emit=parsed_data['enderEmit']['CEP'],
        xMun_emit=parsed_data['enderEmit']['xMun'],UF_emit=parsed_data['enderEmit']['UF'],fone_emit=parsed_data['enderEmit']['fone'],
        CNPJ_emit=cnpj_emit,IE_emit=parsed_data['emit']['IE'],IEST_emit=parsed_data['emit']['IEST'],
        
        xNome=parsed_data['dest']['xNome'],CNPJ_dest=cnpj_dest,
        IE=parsed_data['dest']['IE'],xLgr=parsed_data['enderDest']['xLgr'],nro=parsed_data['enderDest']['nro'],
        xBairro=parsed_data['enderDest']['xBairro'],cep_dest=cep_dest,xMun=parsed_data['enderDest']['xMun'],
        UF=parsed_data['enderDest']['UF'],fone=parsed_data['enderDest']['fone'],
        
        modFrete=parsed_data['modFrete'],transporta_nome=transporta_nome,cnpj_tranp=cnpj_tranp,
        UF_transp=parsed_data['transporta']['UF'],xMun_transp=parsed_data['transporta']['xMun'],
        xEnder_transp=parsed_data['transporta']['xEnder'],IE_transp=parsed_data['transporta']['IE'],
        qVol_transp=parsed_data['vol']['qVol'],esp_transp=parsed_data['vol']['esp'],pesoB_transp=pesoB,
        pesoL_transp=pesoL,
        
        nProt_infProt=parsed_data['infProt']['nProt'],
        
        
        bar_code=parsed_data['BarCode'],
        )
    file.write(render)
    file.close()
    
def SavePDF():
    pdfkit.from_file('core/templates/output/output.html','output.pdf')
    
def Format_CPF_CNPJ(_input):
    
    if len(_input) < 11:
        """ CPF """
        _input = _input.zfill(11)
        cpf = '{}.{}.{}-{}'.format(_input[:3], _input[3:6], _input[6:9], _input[9:])
        return cpf
    elif len(_input) > 11:
        """ CNPJ """
        _input = _input.zfill(14)
        cnpj = '{}. {}. {}/{}-{}'.format(_input[:2], _input[2:5], _input[5:8], _input[8:12], _input[12:])
        return cnpj

def Format_CEP(_input):
    if len(_input) <= 8:
        _input = _input.zfill(8)
        cep = '{}-{}'.format(_input[:5], _input[5:])
        print(cep)
        return cep
    
def String_replacement(obj, toreplace, replacement):
    value = obj.replace(toreplace, replacement) 
    return value