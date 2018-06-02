#!/usr/local/bin/jython
# -*- coding: utf-8 -*-
from java.awt import GridLayout
from java.awt import BorderLayout
from javax.swing import JButton
from javax.swing import JFrame
from javax.swing import JOptionPane
from javax.swing import JPanel
from javax.swing import JLabel
from javax.swing import JCheckBox
from javax.swing import JTextField
from javax.swing import JFileChooser
from javax.swing import JTextArea
from javax.swing import JDialog
from javax.swing import JScrollPane
from javax.swing import BorderFactory
from javax.swing.filechooser import FileNameExtensionFilter
from java.awt import *
from java.lang import *
from java.util import *
import subprocess


class Interfaz(JFrame):

    def __init__(self):
        super(Interfaz, self).__init__()
        self.filename=''
        self.initUI()

    def initUI(self):

        self.panel = JPanel()
        self.panel.setLayout(GridLayout(6, 3))
        self.panel.setBorder(BorderFactory.createEmptyBorder(10,10,10,10))

        labelVacio1 = JLabel(' ')
        labelVacio2 = JLabel(' ')
        labelVacio3 = JLabel(' ')
        labelVacio4 = JLabel(' ')
        labelVacio5 = JLabel(' ')
        labelVacio6 = JLabel(' ')
        labelVacio7 = JLabel(' ')
        labelVacio8 = JLabel(' ')
        labelVacio9 = JLabel(' ')
        labelVacio10 = JLabel(' ')
        labelVacio11 = JLabel(' ')
        labelVacio12 = JLabel(' ')
        labelVacio13 = JLabel(' ')
        labelVacio14 = JLabel(' ')
        labelVacio15 = JLabel(' ')
        labelVacio16 = JLabel(' ')
       

        labelURL = JLabel(' Introduzca las URL que desee analizar:')
        chkboxSync = JCheckBox('Sincronizacion de cookies')
        self.textfieldURL = JTextField(15)
        chkboxResp = JCheckBox('Restauracion de cookies')
        labelFichero = JLabel(' O seleccione un fichero que las contenga:')
        

        self.area = JTextArea()
        pane = JScrollPane()
        pane.getViewport().add(self.area)

        panelFichero = JPanel()
        panelFichero.setLayout(None)
        buttonFichero = JButton("Seleccionar fichero", actionPerformed=self.open)
        buttonFichero.setBounds(10,0,200,25)
        panelFichero.add(buttonFichero)
        buttonEjecutar = JButton("Ejecutar", actionPerformed=self.ejecutar)
        
        buttonEjecutar.setFont(Font("Tahoma", Font.BOLD, 24))

        
        self.panel.add(labelURL)
        self.panel.add(labelVacio4)
        self.panel.add(chkboxSync) 
 
        self.panel.add(self.textfieldURL)
        self.panel.add(labelVacio6)
        self.panel.add(chkboxResp)
 
 
        self.panel.add(labelFichero)
        self.panel.add(labelVacio9)
        self.panel.add(labelVacio10)
 
        self.panel.add(pane)
        self.panel.add(panelFichero)
        #self.panel.add(buttonFichero)
        self.panel.add(labelVacio11)
 
        self.panel.add(labelVacio12)
        self.panel.add(labelVacio13)
        self.panel.add(labelVacio14)
 
        self.panel.add(labelVacio15)
        self.panel.add(buttonEjecutar)
        self.panel.add(labelVacio16)
        

        self.add(self.panel)

        self.setTitle("HERRAMIENTA PARA LA DETECCION DE TECNICAS DE SEGUIMIENTO DE USUARIOS EN LA WEB")
        self.setSize(1000, 450)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setLocationRelativeTo(None)
        self.setVisible(True)


    def open(self, e):
        filechooser = JFileChooser()
        filter = FileNameExtensionFilter("c files", ["c"])
        filechooser.addChoosableFileFilter(filter)
        ret = filechooser.showDialog(self.panel, "Elegir fichero")
        if ret == JFileChooser.APPROVE_OPTION:
            file = filechooser.getSelectedFile()
            text = self.readFile(file)
            self.area.setText(text)

    def readFile(self, file):
        filename = file.getCanonicalPath()
        self.filename= filename
        f = open(filename, "r")
        text = f.read()
        return text

    def ejecutar(self, e):
    	JOptionPane.showMessageDialog(self.panel, "Ejecutando...\n Espere unos minutos.", "Info", JOptionPane.INFORMATION_MESSAGE)   
        print("Ejecutando...")
        url= self.textfieldURL.getText()
        fichero = self.area.getText()
        urls_finales=''

        if url == '' and fichero == '':
        	self.error()
        	return
        elif url != '' and fichero != '':
        	print("Hay url y fichero")
        	urls_finales = url+"\n"+fichero
        	#self.writeFile(urls,1)
        	
        elif fichero != '':
        	print("Hay fichero")
        	urls_finales =fichero
        	#self.writeFile(fichero,1)
        	
        elif url != '':
        	print ("Hay url")
        	self.filename="url"
        	urls_finales=url
        	#self.writeFile(url,1)
        	
        else:
        	print("Ha habido un error")

        self.writeFile(urls_finales,1)
        f = open("bbdd.txt","w")
        f.write(self.filename+"1\n")
        f.close()
        subprocess.call("python demo.py", shell= True)
        self.writeFile(urls_finales,2)
        f = open("bbdd.txt","a")
        f.write(self.filename+"2")
        f.close()
        subprocess.call("python demo.py", shell=True)
        subprocess.call("python rastreo_analisis.py", shell= True)
        
        self.initResultados()
    
    def initResultados(self):
    	diag = JFrame()
    	self.lineas=list()
    	self.areaResultados = JTextArea()
    	numLineas = self.readResultados()
    	
    	panelResultados = JPanel()
    	#panelResultados.setAutoscrolls(True)
    	panelResultados.setBorder(BorderFactory.createEtchedBorder())
        panelResultados.setLayout(GridLayout(0,1))

        
    
    	pane = JScrollPane(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED)
    	pane.viewport.view = self.areaResultados

        #pane.getViewport().add(panelResultados)


    	# labels = list()
    	# for i in range(0,numLineas-1):
    	# 	labels.append(JLabel(''))
    	# 	labels[i].setText(self.lineas[i])
    	# 	area.setText(self.lineas[i])
    		#panelResultados.add(labels[i])
    	#panelResultados.add(JLabel('Holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))

        diag.setTitle("RESULTADOS OBTENIDOS")
        
    	diag.setSize(1000, 450)
    	diag.setLayout(BorderLayout())
    	diag.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
    	diag.setLocationRelativeTo(None)
    	diag.setVisible(True)

    	panelResultados.add(pane)
    	diag.add(panelResultados, BorderLayout.CENTER)

    def readResultados(self):
    	count = 0
    	f = open("resultados.txt", "r")
    	resultados = f.read()
    	self.areaResultados.setText(resultados)

    	for linea in f:
    		self.lineas.append(linea)
    		count +=1 

    	return count


    def writeFile(self, urls,crawl):
    	self.filename = self.filename.replace(".txt", '')
        f = open("URLs.txt", "w")
        f.write(self.filename+str(crawl)+".txt"+'\n')
        f.write(urls)
        f.close()   
  
        
        #subprocess.call("python rastreo_analisis.py", shell= True)
    def error(self):
    	JOptionPane.showMessageDialog(self.panel, "Debes introducir una URL o un fichero", "Error", JOptionPane.ERROR_MESSAGE)   



if __name__ == '__main__':
    Interfaz()
