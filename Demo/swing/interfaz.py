#!/usr/local/bin/jython
# -*- coding: utf-8 -*-


from java.awt import GridLayout
from javax.swing import JButton
from javax.swing import JFrame
from javax.swing import JOptionPane
from javax.swing import JPanel
from javax.swing import JLabel
from javax.swing import JCheckBox
from javax.swing import JTextField
from javax.swing import JFileChooser
from javax.swing import JTextArea
from javax.swing import JScrollPane
from javax.swing import BorderFactory
from javax.swing.filechooser import FileNameExtensionFilter
from java.awt import *
from java.lang import *
from java.util import *

import ejemplo

class Interfaz(JFrame):
    

    def __init__(self):
        super(Interfaz, self).__init__()

        self.initUI()

    def initUI(self):

        self.panel = JPanel()
        self.panel.setLayout(GridLayout(5, 2))

        
        labelURL = JLabel('Introduzca las URL que desee analizar:')
        chkboxSync = JCheckBox('Sincronizacion de cookies')
        textfieldURL = JTextField(15)
        chkboxResp = JCheckBox('Restauracion de cookies')
        labelFichero = JLabel('O si lo prefiere, seleccione un fichero .txt que las contenga:')
        label6 = JLabel(' ')

        self.area = JTextArea()
        pane = JScrollPane()
        pane.getViewport().add(self.area)

        buttonFichero = JButton("Seleccionar fichero", actionPerformed=self.open)
        buttonEjecutar = JButton("Ejecutar", actionPerformed=self.ejecutar)
        label10 = JLabel(' ')

        
        self.panel.add(labelURL)
        self.panel.add(chkboxSync)
        self.panel.add(textfieldURL)
        self.panel.add(chkboxResp)
        self.panel.add(labelFichero)
        self.panel.add(label6)
        self.panel.add(pane)
        self.panel.add(buttonFichero)
        self.panel.add(buttonEjecutar)
        self.panel.add(label10)
        

        self.add(self.panel)

        self.setTitle("HERRAMIENTA PARA LA DETECCION DE TECNICAS DE SEGUIMIENTO DE USUARIOS EN LA WEB")
        self.setSize(950, 450)
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
        f = open(filename, "r")
        text = f.read()
        return text

    def ejecutar(self, e):
        print("Ejecutando...")
        ejemplo.imprimir()

        

if __name__ == '__main__':
    Interfaz()
