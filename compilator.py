import sys
#Tokens
class Token:
   id = 0
   nmr_i = 1
   nmr_f = 2
   op = 3
   timida = 4
   pt = 5
   vrigula = 6
   cabo = 7
   abr_prt = 8
   fch_prt = 9
   abr_cv = 10
   fch_cv = 11
   abr_ch = 12
   fch_ch = 13
   balela = 14
   comp = 15
   igl = 16
   cudigo=17
   nl = 18
   lixo = 19
   tipo = 20
   se = 21
   enqt = 22
   do = 23
   els = 24
   pega_a_vizao = 25
   kero_ve = 26
   txt = 27
   def __init__(self,id=0,text=''):
       self.id = id
       self.text = text
   def __str__(self):
       return("[" + str(self.id) + "," + self.text + "]")
 
#Analisador Léxico
class AnalL:
   linha_atual=0 
   plr_timidas = ['tah_serto_entao','n1_tah_serto_logo']
   pensa_se = ['pensa_se']
   enquantu = ['enquantu']
   els = ['els']
   fazer = ['fazer']
   pega_a_visao = ['pega_a_visao']
   kero_ve = ['kero_ve']
   tipinho = ['redondo','quebrada','turing']
   pos = -1
   def __init__(self,filename):
       try:
           self.file = open(filename)
           self.content = self.file.read().replace('\t',' ')
       except:
           print('Puta arquivo ruim da porra, deu pra ler n, mau ae')
   def ehTimida(self,text):
       return(text in self.plr_timidas)
   def cabar(self):
       return(self.pos==len(self.content)-1)
   def charVai(self):
       self.pos+=1
       return(self.content[self.pos])
   def ehLetra(self,c):
       return(((ord(c) >= 97) & (ord(c) <= 122)) | ((ord(c) >= 65) & (ord(c) <= 90)))
   def ehDigimon(self,c):
       return ((ord(c) >= 48) & (ord(c) <= 57))
   def ehVrigula(self,c):
       return(c==',')
   def ehPontinho(self,c):
       return (c=='.')
   def ehNada(self,c):
       return (((ord(c) >= 0) & (ord(c) <= 9))  | (c==' '))
   def ehPulaLinha(self,c):
       return (ord(c)==10)
   def ehBalela(self,c):
       return (c=='#')
   def volta(self):
       self.pos-=1
   def ehOperario(self,c):
       return ((c=='-') | (c=='+') | (c=='*') | (c=="/") | (c=='^'))
   def ehComperario(self,c):
       return ((c=='<') | (c=='>'))
   def ehIgualitario(self,c):
       return (c=='=')
   def ehAbrPrt(self,c):
       return (c=='(')
   def ehFchPrt(self,c):
       return (c==')')
   def ehAbrCv(self,c):
       return (c=='{')
   def ehFchCv(self,c):
       return (c=='}')
   def ehAbrCh(self,c):
       return (c=='[')
   def ehFchCh(self,c):
       return (c==']')
   def ehBarra(self,c):
       return (c=='\\')
   def ehAspas(self,c):
       return (c=='"')
   def PrecVolta(self,c):
       return ( (ord(c)>=40 & ord(c)<=47) & (ord(c)>=123 & ord(c)<=125) )       
   def TokenAdelante(self):
       s=0
       text=''
       while (9*5==45):
           
           if(s==0):
               if (self.cabar()):
                   return Token(Token.cabo,"")
               c = self.charVai()
               #print(c,ord(c))
               if(self.ehLetra(c)):
                   #print('bora')
                   s=1
                   text+= c
               elif(self.ehDigimon(c)):
                   s=3
                   text+= c
               elif(self.ehBalela(c)):
                   s=2
                   text+= c
               elif(self.ehOperario(c)):
                   text+= c
                   return Token(Token.op,text)
               elif(self.ehNada(c)):
                   s=0
               elif(self.ehVrigula(c)):
                   text+= c
                   return Token(Token.vrigula,text)
               elif(self.ehPontinho(c)):
                   text+=c
                   return Token(Token.pt,text)
               elif(self.ehComperario(c)):
                   text+=c
                   c=self.charVai()
                   if(c=='='):
                       text+=c
                       return Token(Token.comp,text)
                   else:
                       self.volta()
                   return Token(Token.comp,text)
               elif(self.ehAbrPrt(c)):
                   text+=c
                   return Token(Token.abr_prt,text)
               elif(self.ehFchPrt(c)):
                   text+=c
                   return Token(Token.fch_prt,text)
               elif(self.ehAbrCv(c)):
                   text+=c
                   return Token(Token.abr_cv,text)
               elif(self.ehFchCv(c)):
                   text+=c
                   return Token(Token.fch_cv,text)
               elif(self.ehAbrCh(c)):
                   text+=c
                   return Token(Token.abr_ch,text)
               elif(self.ehFchCh(c)):
                   text+=c
                   return Token(Token.fch_ch,text)
               elif(self.ehPulaLinha(c)):
                   text='\n'
                   return Token(Token.nl,text)
               elif(self.ehIgualitario(c)):
                   text+=c
                   c = self.charVai()
                   if(c=='='):
                       text+=c
                       return Token(Token.comp,text)
                   else:
                       self.volta()
                   return Token(Token.igl,text)
               elif(self.ehBarra(c)):
                   text+=c
                   c = self.charVai()
                   if(c=='n'):
                       text+=c
                       return Token(Token.nl,text)
                   else:
                       print('olha:1',c)
                       return Token(Token.lixo,text)
               elif(self.ehAspas(c)):
                   text+=c
                   s=5
               else:
                   print('olha2',ord(c))
                   return Token(Token.lixo,text)
           elif(s==1):
               c = self.charVai()
               if((self.ehLetra(c)) | (self.ehDigimon(c)) | (c=='_')):
                   s=1
                   text+=c
               else:
                   temp=text
                   text=''
                   #elif(self.ehNada(c)):
                   if(self.PrecVolta(c)):
                       self.volta()
                       if(self.ehTimida(temp)):
                           return Token(Token.timida,temp)
                       elif(temp=='cudigo'):
                           return Token(Token.cudigo,temp)
                       elif(temp in self.pensa_se):
                           return Token(Token.se,temp)
                       elif(temp in self.enquantu):
                           return Token(Token.enqt,temp)
                       elif(temp in self.pega_a_visao):
                           return Token(Token.pega_a_vizao,temp)
                       elif(temp in self.els):
                           return Token(Token.els,temp)
                       elif(temp in self.fazer):
                           return Token(Token.do,temp)
                       elif(temp in self.kero_ve):
                           return Token(Token.kero_ve,temp)
                       elif(temp in self.tipinho):
                           return Token(Token.tipo,temp)
                       else:
                           #print(repr(temp))
                           return Token(Token.id,temp)
                   else:
                       if(self.ehTimida(temp)):
                           return Token(Token.timida,temp)
                       elif(temp=='cudigo'):
                           return Token(Token.cudigo,temp)
                       elif(temp in self.pensa_se):
                           return Token(Token.se,temp)
                       elif(temp in self.enquantu):
                           return Token(Token.enqt,temp)
                       elif(temp in self.pega_a_visao):
                           return Token(Token.pega_a_vizao,temp)
                       elif(temp in self.els):
                           return Token(Token.els,temp)
                       elif(temp in self.fazer):
                           return Token(Token.do,temp)
                       elif(temp in self.kero_ve):
                           return Token(Token.kero_ve,temp)
                       elif(temp in self.tipinho):
                           return Token(Token.tipo,temp)
                       else:
                           #print(repr(temp))
                           return Token(Token.id,temp)
           elif(s==2):
               c = self.charVai()
               text+=c
               if(self.ehBalela(c)):
                   return Token(Token.balela,text)
           elif(s==3):
               c=self.charVai()
               if(self.ehDigimon(c)):
                   text+=c
               elif(self.ehPontinho(c)):
                   text+=c
                   s=4
               elif(self.ehNada(c)):
                   return Token(Token.nmr_i,text)
               else:
                   self.volta()
                   return Token(Token.nmr_i,text)
                   #raise Exception('Era numero, agr n eh mais, q balbudia eh essa?')
           elif(s==4):
               c=self.charVai()
               if(self.ehDigimon(c)):
                   text+=c
               elif(self.ehNada(c)):
                   return Token(Token.nmr_f,text)
               else:
                   self.volta()
                   return Token(Token.nmr_f,text)
                   #raise Exception('Era numero, agr n eh mais, q balbudia eh essa?')
           elif(s==5):
               c=self.charVai()
               while(self.ehAspas(c)==False):
                   if(self.cabar()):
                       return Token(Token.cabo,text)
                   text+=c
                   c=self.charVai()
               text+=c
               return Token(Token.txt,text)
                  
#Analisador Sintatico
class AnalS:
   linha_atual=0
   qtdIdent='    '
   """
  
  
   PRECISA IMPLEMENTAR ESCRITA
   E LEITURA
  
  
   """
   cod_java = "public class "
   lex: AnalL
   tipinho = ['redondo','quebrada','turing']
   conversao_tipo = {'redondo':'int','quebrada':'double','turing':'boolean'}
   varas = []
   def __init__(self,l):
       self.lex = l
   def programa(self):
       t = self.lex.TokenAdelante()
       #print(t.id)
       if(t.id==Token.cudigo):
           t=self.lex.TokenAdelante()
           if(t.id==Token.id):
               self.cod_java += t.text
               t=self.lex.TokenAdelante()
               if(t.id==Token.abr_cv):
                   #self.cod_java+='import java.util.Scanner;'
                   self.cod_java+="{\n"+self.qtdIdent+"public static void main(String[] args){\n"
                   self.linha_atual+=2
                   self.qtdIdent+='    '
                   self.cod_java+=self.qtdIdent+'java.util.Scanner sc = new java.util.Scanner(System.in);'
                   t = self.lerLinhas()
                   self.cod_java+='\n}'
                   self.linha_atual+=1
                   return(self.cod_java)
               else:
                   print(t.id,repr(t.text))
                   raise Exception('Abre a chave, coe')
           else:
               print(t.id,repr(t.text))
               raise Exception('Aqui eh pra vc dar nome ao teu filho bixo')
       else:
           print(t.id,repr(t.text))
           raise Exception('Maluco, jurava que viria um codigo aqui')
   def lerLinhas(self,precisaIr=True,t=None):
       
       if(precisaIr):
           t = self.lex.TokenAdelante()
       if(t.id==Token.fch_cv):
           self.qtdIdent=self.qtdIdent[:-4]
           for i in range(4):
               if(self.cod_java[-1:]==' '):
                   self.cod_java = self.cod_java[:-1]
           self.cod_java+='}'
           return t
       if(t.id==Token.nl):
           self.cod_java+='\n'+self.qtdIdent
           self.linha_atual+=1                 
           return self.lerLinhas()
       elif(t.id==Token.tipo):
           self.cod_java+=self.conversao_tipo[t.text]+' '
           t = self.declara()
           #print(type(t))
           if(t.id==Token.nl):
               self.cod_java+=';\n'+self.qtdIdent
               return self.lerLinhas()
           else:
               print(t.id,t.text)
               raise Exception('Não acreditei que chegariamos a esse ponto\nAh que ponto chegamos')           
       elif(t.id==Token.id):
           if(t.text in self.varas):
               self.cod_java += t.text
               t = self.lex.TokenAdelante()
               if(t.id==Token.igl):
                   self.cod_java+=' = '
                   t=self.ehOperacaoLavaJato()
                   self.cod_java+=';\n'+self.qtdIdent
                   return self.lerLinhas()
               else:
                   raise Exception('Ma num era um igual aqui nao po?')
           else:
               print(t.id,repr(t.text))
               raise Exception('Declara a var caraio, ja faleii')
       elif((t.id==Token.enqt) | (t.id==Token.se)):
           if (t.id==Token.enqt):
               self.cod_java += 'while '
               ehse = False
           else:
               self.cod_java += 'if '
               ehse = True
           t = self.condicional()
           if(t.id==Token.abr_cv):
               self.cod_java+='{'
               self.qtdIdent+='    '
               t = self.lerLinhas()
               t = self.lex.TokenAdelante()
               if ((t.id==Token.els) & (ehse==True)):
                   self.cod_java+='else'
                   t = self.lex.TokenAdelante()
                   if(t.id==Token.abr_cv):
                       self.qtdIdent+='    '
                       self.cod_java+='{'
                       t = self.lerLinhas()
                       return self.lerLinhas()
                   else:
                       print(t.id,repr(t.text))
                       raise Exception('Falto tá chavão!')
               else:
                   return self.lerLinhas(False,t)
           else:
               print(t.id,repr(t.text))
               raise Exception('Falto tá chavão!')
              
       elif(t.id==Token.do):
           self.cod_java+='do'
           t = self.lex.TokenAdelante()
           if(t.id==Token.abr_cv):
               self.cod_java+='{'
               t = self.lerLinhas()
               t = self.lex.TokenAdelante()
               if(t.id==Token.enqt):
                   self.cod_java+='while '
                   t = self.condicional()
                   return self.lerLinhas(False,t)
               else:
                   print(t.id,repr(t.text))
                   raise Exception('Eh pra do mas n é pra while? Ai me complica neh')
           else:
               print(t.id,repr(t.text))
               raise Exception('Falto tá chavão!!')
          
       elif(t.id==Token.kero_ve):
           self.cod_java+="System.out.println"
           t = self.lex.TokenAdelante()
           if(t.id==Token.abr_prt):
               self.cod_java+='('
               t=self.lex.TokenAdelante()
               while(t.id!=Token.fch_prt):
                   if(t.id==Token.cabo):
                       print(t.id,repr(t.text))
                       raise Exception('minino, tava esperando vc fecha parenteses ate agr')
                   if((self.cod_java[-1:]!='(') & (self.cod_java[-1:]!='+')):
                       if(t.text=='+'):
                           self.cod_java+=t.text
                       else:
                           raise Exception('Digita ++++++++++++') 
                       t=self.lex.TokenAdelante()
                   else:
                       if(t.id==Token.txt):
                           self.cod_java+=t.text
                           t=self.lex.TokenAdelante()
                       else:
                           t = self.ehOperacaoLavaJato(False,t)
               self.cod_java+=');'
               self.lerLinhas()               
           else:
               print(t.id,repr(t.text))
               raise Exception('Pfv abre parenteses aqui moço')
      
       else:
           print(t.id,repr(t.text))
           raise Exception('Comecando linha com coisa nd a ve amigao? NAO PODIII')
      
   def declara(self):
       t = self.lex.TokenAdelante()
       if(t.id==Token.id):
           self.varas.append(t.text)
           self.cod_java+=t.text
           t = self.lex.TokenAdelante()
           if(t.id==Token.vrigula):
               self.cod_java+=', '
               return self.declara()
           elif(t.id==Token.igl):
               self.cod_java+=' = '
               t = self.ehOperacaoLavaJato()
               if(t.id==Token.nl):
                   #self.cod_java+='\n'
                   #print(type(t))
                   return t
               elif(t.id==Token.vrigula):
                   self.cod_java+=', '
                   return self.declara()
               else:
                   print(t.id,repr(t.text))
                   raise Exception('Ja deu valor ja, cabo amigão, vai pra casa')
           elif(t.id==Token.nl):
               #self.cod_java+='\n'
               return Token(id=t.id,text=t.text)
           else:
               print(t.id,repr(t.text))
               raise Exception('vc deu nome pro bixo e ja ta achando que eh dono ne?')
       else:
           print(t.id,repr(t.text))
           raise Exception('DAH, NOME, PRA, CRIANçAAAAAAAAAAAA')
   def condicional(self):
       t = self.lex.TokenAdelante()
       if(t.id==Token.abr_prt):
           self.cod_java+='('
           t=self.ehOperacaoLavaJato()
           if(t.id==Token.comp):
               self.cod_java+=t.text
               #print(t.id,'aqi',repr(t.text))
               #print(t.id,'aqui',repr(t.text))
               t=self.ehOperacaoLavaJato()
               if(t.id==Token.fch_prt):
                   self.cod_java+=')'
                   t=self.lex.TokenAdelante()
                   return t
               else:
                   print(t.id,repr(t.text))
                   raise Exception('FECHA O PARANTESIS')
           else:
               print(t.id,repr(t.text))
               raise Exception('Vai compara sem nem comparar? Q q eh isso?')
       else:
           print(t.id,repr(t.text))
           raise Exception('Vai compara sem nem abrir o comparar? Q q eh isso?')
   def ehOperacaoLavaJato(self,precisaIr=True,t=None):
       if(precisaIr):
           t = self.lex.TokenAdelante()
       if(t.id==Token.abr_prt):
           self.cod_java+='('
           t = self.ehOperacaoLavaJato()
           if(t.id==Token.fch_prt):
               self.cod_java+=')'
               t=self.lex.TokenAdelante()
               if(t.id==Token.op):
                   self.cod_java+=t.text
                   t = self.ehOperacaoLavaJato()
                   #print(t.id,repr(t.text))
                   return t
           else:
               print(t.id,repr(t.text))
               raise Exception('Num fecho essa demonia')
       if((t.id==Token.id) | (t.id in [Token.nmr_f,Token.nmr_i]) | (t.id==Token.pega_a_vizao)):
           if(t.id==Token.pega_a_vizao):
               t=self.lex.TokenAdelante()
               if(t.id==t.abr_prt):
                   t=self.lex.TokenAdelante()
                   if(t.text in self.tipinho):
                       self.cod_java+='sc.next'+self.conversao_tipo[t.text][0].upper()+self.conversao_tipo[t.text][1:]+'('
                       t = self.lex.TokenAdelante()
                       if(t.id!=Token.fch_prt):
                           print(t.id,repr(t.text))
                           raise Exception('KEDE PARENTESES MALUCO?')
                       self.cod_java+=')'
                   else:
                       print(t.id,repr(t.text))
                       raise Exception('Soh trabalho com tipos')
               else:
                   print(t.id,repr(t.text))
                   raise Exception('Abre o parenteses bixo, se nao eh sem visao')
           elif(t.id==Token.id):
               if(t.text not in self.varas):
                   print(t.id,repr(t.text))
                   raise Exception('Declara essse merda, pf')
               self.cod_java+=t.text
           else:
               self.cod_java+=t.text
           t = self.lex.TokenAdelante()
           while(t.id==Token.op):
               self.cod_java+=t.text
               t = self.lex.TokenAdelante()
               if((t.id==Token.id) | (t.id in [Token.nmr_f,Token.nmr_i])):
                   self.cod_java+=t.text
                   t = self.lex.TokenAdelante()
               else:
                   print(t.id,repr(t.text))
                   raise Exception('Num sabe nem matematica em, burrao')
           #print(t.id,repr(t.text))
           return t
       else:
           print(t.id,repr(t.text))
           raise Exception('Era pra ter um valor aqui poxa')

if(len(sys.argv)>1):
    filename=sys.argv[1]
    l = AnalL(filename)
    #print('\n\n\n\n\n\n\n',l.content,'\n\n\n\n\n')
    o=AnalS(l)
    a = o.programa()
    print('\n'+a+'\n')
    if(len(sys.argv)>2):
        destiny = sys.argv[2]
    else:
        destiny = 'saida'
    f=open(destiny+'.java','w')
    f.write(a)

else:
    print('Por favor diga qual o arquivo origem')
