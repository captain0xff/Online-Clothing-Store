import os
import pkg_resources

class Packages:
   def __init__(self,required_packages_dict):
      self.required_packages_dict=required_packages_dict

   def get_installed_versions(self):
      installed_packages = pkg_resources.working_set
      self.installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
         for i in installed_packages])
      self.installed_packages_dict={}
      for i in self.installed_packages_list:
         info=i.split('==')
         self.installed_packages_dict[info[0]]=info[1]

   def check_packages(self):
      self.packages_found=[]
      self.packages_not_found=[]
      self.old_packages=[]
      self.correct_packages=[]
      for i in self.required_packages_dict:
         if i in self.installed_packages_dict:
            self.packages_found.append(i)
         else:
            self.packages_not_found.append(i)
      for i in self.packages_found:
         if self.compare_version(self.installed_packages_dict[i],self.required_packages_dict[i]):
            self.old_packages.append(i)
         else:
            self.correct_packages.append(i)

   def compare_version(self,installed_version,required_version):
      installed_version_list=installed_version.split('.')
      required_version_list=required_version.split('.')
      fail=False
      for i in range(len(installed_version_list)):
         if int(installed_version_list[i])<int(required_version_list[i]):
            fail=True
            break
      return fail

   def show_status(self):
      for i in self.packages_not_found:
         msg='{name} is not found. Please install the module.'
         msg=msg.format(name=i)
         print(msg)
      for i in self.old_packages:
         msg='{name} is too old! Please consider updating the module.'
         msg=msg.format(name=i)
         print(msg)
      for i in self.correct_packages:
         msg='{name} is found!'
         msg=msg.format(name=i)
         print(msg)
      print()

   def install_missing_packages(self):
      if self.packages_not_found:
         op1=input('Do you want to install the missing packages? (y/N): ')
         if op1 in 'Yy':
            for i in self.packages_not_found:
               cmd='pip install "{name}"'.format(name=i)
               os.system(cmd)
      if self.old_packages:
         op2=input('Do you want to update the old packages? (y/N): ')
         if op2 in 'Yy':
            for i in self.old_packages:
               cmd='pip install "{name}>={version}"'.format(name=i,version=self.required_packages_dict[i])
               print(cmd)
               os.system(cmd)
      print('Done!!!')

   def main(self):
      self.get_installed_versions()
      self.check_packages()
      self.show_status()
      self.install_missing_packages()

#Requirements
requirements={
   'pysimplegui':'4.50.0',
   'mysql-connector-python':'8.0.26',
   'matplotlib':'3.4.3',
   'mplcursors':'0.5.1'
}

if __name__=='__main__':
   my_packages=Packages(requirements)
   my_packages.main()