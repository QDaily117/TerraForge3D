import sys
import os
import winreg

import requests
import time
import urllib

import datetime

from zipfile import ZipFile

def GetSystemEnvironmentVariable(name):
    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"System\CurrentControlSet\Control\Session Manager\Environment")
    try:
        return winreg.QueryValueEx(key, name)[0]
    except:
        return None

def GetUserEnvironmentVariable(name):
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment")
    try:
        return winreg.QueryValueEx(key, name)[0]
    except:
        return None

def DownloadFile(url, filepath):
    path = filepath
    filepath = os.path.abspath(filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
    if (type(url) is list):
        for url_option in url:
            print("Downloading", url_option)
            try:
                DownloadFile(url_option, filepath)
                return
            except urllib.error.URLError as e:
                print(f"URL Error encountered: {e.reason}. Proceeding with backup...\n\n")
                os.remove(filepath)
                pass
            except urllib.error.HTTPError as e:
                print(f"HTTP Error  encountered: {e.code}. Proceeding with backup...\n\n")
                os.remove(filepath)
                pass
            except:
                print(f"Something went wrong. Proceeding with backup...\n\n")
                os.remove(filepath)
                pass
        raise ValueError(f"Failed to download {filepath}")
    if not(type(url) is str):
        raise TypeError("Argument 'url' must be of type list or string")

    with open(filepath, 'wb') as f:
        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        response = requests.get(url, headers=headers, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            startTime = time.time()
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                
                try:
                    done = int(50*downloaded/total) if downloaded < total else 50
                    percentage = (downloaded / total) * 100 if downloaded < total else 100
                except ZeroDivisionError:
                    done = 50
                    percentage = 100
                elapsedTime = time.time() - startTime
                estimatedTime = 0.0
                try:
                    avgKBPerSecond = (downloaded / 1024) / elapsedTime
                    estimatedTime = ( (total - downloaded) / (avgKBPerSecond*1024) )
                except ZeroDivisionError:
                    avgKBPerSecond = 0.0
                    estimatedTime = -1.0 # representation of infinite
                avgSpeedString = '{:.2f} KB/s'.format(avgKBPerSecond)
                estimatedTimeString = FormatTime(estimatedTime)
                if (avgKBPerSecond > 1024):
                    avgMBPerSecond = avgKBPerSecond / 1024
                    avgSpeedString = '{:.2f} MB/s'.format(avgMBPerSecond)
                sys.stdout.write('\r[{}{}] {:.2f}% ({}) (Estimated Time: {})    '.format('█' * done, '.' * (50-done), percentage, avgSpeedString, estimatedTimeString))
                sys.stdout.flush()
    sys.stdout.write('\n')

def UnzipFile(filepath, deleteZipFile=True):
    zipFilePath = os.path.abspath(filepath) # get full path of files
    zipFileLocation = os.path.dirname(zipFilePath)

    zipFileContent = dict()
    zipFileContentSize = 0
    with ZipFile(zipFilePath, 'r') as zipFileFolder:
        for name in zipFileFolder.namelist():
            zipFileContent[name] = zipFileFolder.getinfo(name).file_size
        zipFileContentSize = sum(zipFileContent.values())
        extractedContentSize = 0
        startTime = time.time()
        for zippedFileName, zippedFileSize in zipFileContent.items():
            UnzippedFilePath = os.path.abspath(f"{zipFileLocation}/{zippedFileName}")
            os.makedirs(os.path.dirname(UnzippedFilePath), exist_ok=True)
            if os.path.isfile(UnzippedFilePath):
                zipFileContentSize -= zippedFileSize
            else:
                zipFileFolder.extract(zippedFileName, path=zipFileLocation, pwd=None)
                extractedContentSize += zippedFileSize
            try:
                done = int(50*extractedContentSize/zipFileContentSize)
                percentage = (extractedContentSize / zipFileContentSize) * 100
            except ZeroDivisionError:
                done = 50
                percentage = 100
            elapsedTime = time.time() - startTime            
            estimatedTime = 0
            try:
                avgKBPerSecond = (extractedContentSize / 1024) / elapsedTime
                estimatedTime = (zipFileContentSize - extractedContentSize) / (avgKBPerSecond * 1024)
            except ZeroDivisionError:
                avgKBPerSecond = 0.0
                estimatedTime = -1.0
            estimatedTimeString = FormatTime(estimatedTime)
            avgSpeedString = '{:.2f} KB/s'.format(avgKBPerSecond)
            if (avgKBPerSecond > 1024):
                avgMBPerSecond = avgKBPerSecond / 1024
                avgSpeedString = '{:.2f} MB/s'.format(avgMBPerSecond)
            sys.stdout.write('\r[{}{}] {:.2f}% ({}) (Estimated Time: {})     '.format('█' * done, '.' * (50-done), percentage, avgSpeedString, estimatedTimeString))
            sys.stdout.flush()
    sys.stdout.write('\n')

    if deleteZipFile:
        os.remove(zipFilePath) # delete zip file

def FormatTime(seconds):
    if seconds < 0 or seconds > 86400:
        return "> 1 day" # OR return "More than a day!"
    if seconds == 0:
        return "Finished!" # OR return "0s"
    h = int(seconds // 3600)
    m = int(seconds % 3600 // 60)
    s = int(seconds % 3600 % 60)
    formatedTime = ""
    if h > 0:
        formatedTime += "{:02d}h ".format(h)
    if m > 0 or h > 0:
        formatedTime += "{:02d}m ".format(m)
    formatedTime += "{:02d}s".format(s)
    return formatedTime