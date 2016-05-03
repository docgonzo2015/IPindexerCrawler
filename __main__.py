#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  url2rang.py
#
#  Copyright 2016 bop <bop.technology@mail.ru>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import argparse
import socket
import urlparse
import urllib
import urllib2
import re

import sys

# write string to file
def file_put_contents(filename, string, mode='a'):
    myFile = open(filename, mode)
    myFile.write(string)
    myFile.close()

# kill duplikates from a list
def dup_kill(mylist):
    newlist = []
    for i in mylist:
        if i not in newlist:
            newlist.append(i)
    return newlist

def get_page(url, data=None, timeout=5, **kwargs):
    try:
        tmp = urllib2.urlopen(url, data, timeout)
    except Exception,e:
        print str(e)
        return False
    else:
        return tmp

def cleanhtml(raw_html):
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,' ', raw_html)
  return cleantext

def ipindex(ip):
    index = get_page('http://ipindex.dihe.de/index.php', 'action=Go&q=%s' %ip)
    try:
        match = re.findall(r'<TD>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3} - [\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}</TD>.*</TR>', index.read())
        if match:
            return cleanhtml(match.pop()).strip()
    except:
        sys.exit()
    return False

def ip_range(start_ip,end_ip):
    """
    source: http://cmikavac.net/2011/09/11/how-to-generate-an-ip-range-list-in-python/
    author: in the comments: Murali
    date: September 12, 2014 at 22:40
    """
    start = list(map(int,start_ip.split('.')))
    end = list(map(int,end_ip.split('.')))
    iprange=[]
    while start!=list(map(int,end_ip.split('.'))):
        for i in range(len(start)-1,-1,-1):
            if start[i]<255:
                start[i]+=1
                break
            else:
                start[i]=0
        iprange.append('.'.join(map(str,start)))
    return iprange

def get_ips(string):
    match = re.findall(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}', string)
    if match:
        return match
    else:
        return False

def check_range_size(start_ip, end_ip, msize=255):
    tmp = ip_range(start_ip, end_ip)
    if len(tmp) <= msize:
        return True
    else:
        return False

def resize_rang(start_ip, end_ip, size):
    tmp = ip_range(start_ip, end_ip)
    new = []
    for c in range(size):
        new.append(tmp[c])
    return new.pop(0), new.pop()

def main(file, max_rang_size, resize):
    f = open(file)
    for l in f.readlines():
        try:
            url = l.rstrip().rstrip('/')
            host = urlparse.urlparse(url).netloc
            host = host.replace('www.', '')
            print "-"*80
            print host
        except Exception,e:
            print str(e)
            continue
        try:
            ip = socket.gethostbyname(host)
            print ' ' + ip
        except:
            print ' cant get the host'
            continue
        rang = ipindex(ip)
        # hier noch ein check für zu große ip rangs
        if rang:
            print "  "+rang
            rang_l = get_ips(rang)
            if check_range_size(rang_l[0], rang_l[1], max_rang_size):
                print "  saved"
                file_put_contents('new_rangs.txt', rang + '\n', 'a')
            else:
                print "  to big"
                if resize:
                    print "  .. resize the rang"
                    new_start_ip, new_end_ip = resize_rang(rang_l[0], rang_l[1], max_rang_size)
                    rang = rang.replace(rang_l[1], new_end_ip)
                    print "  resized: " + rang
                    file_put_contents('new_rangs.txt', rang + '\n', 'a')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", type=str, help="The file with urls (one url per line!)")
    parser.add_argument("-m", "--max-rang-size", help="The maximal rang size (default=4294967296(=Total number of IPv4 addresses)) (6400=25*256)", type=int, default=4294967296)
    parser.add_argument("-r", "--resize", help="Resize to big rangs to the max-rang-size", action="store_true")
    args = parser.parse_args()
    main( args.FILE, args.max_rang_size, args.resize )

#EOF