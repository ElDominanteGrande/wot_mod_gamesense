# build script

import os, sys
import compileall
import shutil
import zipfile
import xml.etree.ElementTree as ET
import xml.dom.minidom as xmldom
from pipeline_config import Config as pipeline_cfg

modbasepath = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sources = os.path.join(modbasepath, "sources")
utils = os.path.join(modbasepath, "utils")
build = os.path.join(modbasepath, "build")

configmodulepath = os.path.join(sources, "res", "scripts", "client", "gui", "gamesense", "config.py")
shutil.copy(configmodulepath, utils)
from config import Config as cfg
pipeline_config= pipeline_cfg["pipeline_config"]
mod_config = pipeline_cfg["mod_config"]
repo_config = cfg["repo_info"]

xmlfilename = pipeline_config["meta_xml"]
xmlfilepath = os.path.join(build, xmlfilename)

modname = mod_config["name"]
modnameHR = mod_config["nameHR"]
modauthor = mod_config["author"]
modversion = mod_config["version"]
modext =  mod_config["ext"]
moddescr =  mod_config["descr"]
modfilename = modauthor.lower() + "." + modname + "_" + modversion + modext
modpath = os.path.join(build, modfilename)

wotinstallpath = os.path.abspath(pipeline_config["wot_install_root"])


def searchdirs(path, names):
    """
    Scans recurseively path for dirs with the given names (tuple).
    """
    foundDirs = []

    for root, dirs, files in os.walk(path):
        for curdir in dirs:
            curdirpath = os.path.join(root, curdir)
            print "processing dir: " + curdirpath
            if curdir in names:
                foundDirs.append(curdirpath)

    return foundDirs


def scandirs(path, exts, invert = False):
    """
    Scans recurseively path for files with the given extensions (tuple).
    If invert is true, every file will be returned except those with the extensions given.
    """
    foundFiles = []

    for root, dirs, files in os.walk(path):
        for currentfile in files:
            currentfilepath = os.path.join(root, currentfile)
            print "processing file: " + currentfilepath
            exts = exts
            if currentfile.lower().endswith(exts) and not invert:
                foundFiles.append(currentfilepath)
            elif not currentfile.lower().endswith(exts) and invert:
                foundFiles.append(currentfilepath)

    return foundFiles


def generatexml():

    root = "root"
    idstr = "id"
    version = "version"
    name = "name"
    descr = "description"

    commentid = mod_config["meta_info"]["comment_id"]
    commentversion = mod_config["meta_info"]["comment_version"]
    commentname = mod_config["meta_info"]["comment_name"]
    commentdescr = mod_config["meta_info"]["comment_descr"]

    xmlroot = ET.Element(root)
    comment = ET.Comment(commentid)
    xmlroot.insert(len(xmlroot.getchildren()), comment)

    xmlid = ET.SubElement(xmlroot, idstr)
    xmlid.text = modauthor + "." + modname
    comment = ET.Comment(commentversion)
    xmlroot.insert(len(xmlroot.getchildren()), comment)

    xmlversion = ET.SubElement(xmlroot, version)
    xmlversion.text = modversion
    comment = ET.Comment(commentname)
    xmlroot.insert(len(xmlroot.getchildren()), comment)

    xmlname = ET.SubElement(xmlroot, name)
    xmlname.text = modnameHR
    comment = ET.Comment(commentdescr)
    xmlroot.insert(len(xmlroot.getchildren()), comment)

    xmldescr = ET.SubElement(xmlroot, descr)
    xmldescr.text = moddescr

    parsed = xmldom.parseString(ET.tostring(xmlroot))
    
    with open(xmlfilepath, "w") as xmlfile:
        xmlfile.write(parsed.toprettyxml(indent="\t"))


def build_mod():

    # remove old build dir
    if os.path.isdir(build):
        shutil.rmtree(build)

    # copy workspace to build dir
    shutil.copytree(sources, build)

    # generate xml
    generatexml()

    # generate pycs
    compileall.compile_dir(build)

    # Delete all *.py files
    [os.remove(elem) for elem in scandirs(build, (".py"))]
    
    # remove old *.wotmod file
    if os.path.isfile(modpath):
        os.remove(modpath)

    # create new *.wotmod file
    modzip = zipfile.ZipFile(modpath, mode='w')
    try:
        filestozip = scandirs(build, (modext), True)

        for filetozip in filestozip:
            modzip.write(filetozip, os.path.relpath(filetozip, build))
    finally:
        modzip.close()


def deploy_mod():

    if not pipeline_config["deploy_wotmod"]:
        print("No deploying of mod file.")
        return

    wotmodpath = os.path.join(wotinstallpath, pipeline_config["wot_mod_subfolder"], pipeline_config["wot_cur_version"])

    for root, dirs, files in os.walk(wotmodpath):
        for f in files:
            if modauthor + "." + modname in os.path.basename(f):
                os.remove(os.path.join(root,f))

    shutil.copy(modpath, os.path.join(wotmodpath, modfilename))
    

def clear_python_log():

    if not pipeline_config["clear_python_log"]:
        print("No clearing of Python log.")
        return

    pythonlogpath = os.path.join(wotinstallpath, "python.log")
    # clean log
    if os.path.isfile(pythonlogpath):
        os.remove(pythonlogpath)


if __name__ == "__main__":
    build_mod()
    deploy_mod()
    clear_python_log()