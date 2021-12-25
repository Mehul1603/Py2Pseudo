import re

functions_pseudo={}

def clear_code(s):
    i=0
    while i<len(s):
        if re.match(r'[\W]*$',s[i]) or s[i][0]=='#':
            del s[i]
        else:
            i+=1

def remove_whitespaces(s):
    whitespaces=''
    for j in range(len(s)):
        if s[j]==' ':
            whitespaces+=' '
        else:
            s=s[len(whitespaces):]
            break
    return s, whitespaces

def checkfun(s):
    global functions_pseudo
    t=False
    for i in functions_pseudo.keys():
        pattern=re.compile(i)
        matches=pattern.finditer(s)
        x=0
        for j in matches:
            l=list(s)
            s=j.span()
            if l[s[0]-1+x]==' ':
                l.insert(s[0],'CALL ')
                x+=5
                t=True
            else:
                l.insert(s[0],' CALL ')
                x+=6
                t=True
            s=''
            for k in l:
                s+=k
            
    return s,t

#Main Functions
def read(s):
    x=''
    for j in s:
        if j!='=':
            x+=j
        else:
            break
    s='READ '+x
    return s

def compute(s):
    s,t=checkfun('COMPUTE '+ s)
    return s

def sett(s):
    s,t=checkfun('SET '+ s)    
    return s

def prt(s):
    s='PRINT '+s[6:len(s)-1]
    s,t=checkfun(s)
    return s

def forr(s):
    if re.search(r'range\(',s):
        s=s.split()
        if ',' not in s[3]:
            u=s[3][6:-2]
            return 'FOR {} = 0 to {}'.format(s[1],u)
        else:
            l=''
            for i in range(6,len(s[3])):
                if s[3][i]!=',':
                    l+=s[3][i]
                else:
                    x=i+1
                    break
            u=s[3][x:-2]
                
            s,t=checkfun('FOR {} = {} to {}'.format(s[1],l,u))
            return s
    else:
        s,t = checkfun('FOR' + s[3:-1])
        return s
    
def iff(s):
    s='IF '+s[3:-1] + ' THEN'
    s,t=checkfun(s)
    return s

def eliff(s):
    s='ELIF '+s[5:-1] + ' THEN'
    s,t=checkfun(s)
    return s

def elsee():
    return 'ELSE'

def importt(s):
    return 'IMPORT' + s[6:]

def brecon(s):
    return s.upper()

def ret(s):
    s,t = checkfun('RETURN'+s[6:])
    return s

def fun(lines,l):

    global functions_pseudo
    s=lines[l]
    name=''
    for j in range(4,len(s)):
        if s[j]=='(':
            break
        else:
            name+=s[j]
    
    l+=1
    function_code=''
    
    while l<len(lines):
        code=lines[l]
        st,whitespaces = remove_whitespaces(code)
        if len(whitespaces)<4:
            break
        else:
            function_code+=code[4:]+'\n'
            l+=1
    functions_pseudo[name]=convert_to_pseudo_code(function_code,name,s[4+len(name)+1:-2])
    return l
            
def convert_to_pseudo_code(code,name=False,parameters=None):

    lines=code.split('\n')
    clear_code(lines)
        
    i=0
    while i<len(lines):
    
        lines[i], whitespaces = remove_whitespaces(lines[i])
        
        #READ
        s,t=checkfun(lines[i])
        if re.search('input()',lines[i]) and lines[i][-1]!=':' and not t:
            lines[i]=read(lines[i])
            i+=1
        
        #PRINT
        elif lines[i][0:5]=='print':
            lines[i]=prt(lines[i])
            i+=1
        
        #SET
        elif re.match(r'^[\w]+[\s]?=[\s]?',lines[i]):
            s1=''
            x=lines[i]
            for j in range(len(x)):
                if x[j]!='=':
                    s1+=x[j]
                else:
                    x=x[j+1::]
                    break
            s2=''
            for j in range(len(x)):
                if x[j]==' ' and j==0:
                    continue
                elif not(x[j].isalnum()):
                    break
                else:
                    s2+=x[j]
                    
            s1.lstrip()
            s1.rstrip()
            s2.lstrip()
            s2.rstrip()
            if s1==s2:
                lines[i]=compute(lines[i])
            else:
                lines[i]=sett(lines[i])
            i+=1
                
        #FOR
        elif lines[i][0:3]=='for':
            lines[i]=forr(lines[i])
            i+=1
            
        #IF
        elif lines[i][0:2]=='if':
            lines[i]=iff(lines[i])
            i+=1
            
        #ELIF
        elif lines[i][0:4]=='elif':
            lines[i]=eliff(lines[i])
            i+=1
            
        #ELSE
        elif lines[i][0:-1]=='else':
            lines[i]=elsee()
            i+=1
            
        #import
        elif lines[i][0:6]=='import':
            lines[i]=importt(lines[i])
            i+=1

        #break/continue
        elif lines[i]=='break' or lines[i]=='continue':
            lines[i]=brecon(lines[i])
            i+=1

        #return
        elif lines[i][0:6]=='return':
            lines[i]=ret(lines[i])
            i+=1

        #def
        elif lines[i][0:3]=='def':
            k=fun(lines,i)
            for l in range(k-i):
                del lines[i]
            continue
        
        #COMPUTE
        else:
            lines[i]=compute(lines[i])
            i+=1
        
        lines[i-1]=whitespaces+lines[i-1]
        
    if name and parameters:
        lines.reverse()
        lines.append('Input: '+parameters)
        lines.reverse()
    
    output=''
    for i in lines:
        output+=i+'\n'
    return output
   
with open('PASTE CODE HERE.txt','r') as f:
    code=f.read()
    
code='Pseudocode\n'+convert_to_pseudo_code(code)+'\n\n'
for i,j in functions_pseudo.items():
    code+='Pseudocode for {}\n'.format(i)+j+'\n\n'
print('Pseudo-Code generated')

with open('PASTE CODE HERE.txt','w') as f:
    
    f.write(code)
