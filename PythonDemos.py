import pythoncom
class PythonUtilities:

    _public_methods_=['SplitString']
    _reg_progid_='PythonDemos.Utilities'
    _reg_clsid_=pythoncom.CreateGuid()

    def SplitString(self, val, item=None):
        import string
        if item !=None:
            item=str(item)
        val=str(val)
        return val.split(item)

if __name__=='__main__':
    print ('Registering COM server...')
    import win32com.server.register
    win32com.server.register.UseCommandLine(PythonUtilities)
