from httplib2 import Http
import json
import sys

# Counter variables for fail/success summary.
fail = 0
success = 0
total = 0


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# endpoint tester test if url endpoint is reachable
# apiendpoint : true/false to test API url

def endpointTester(url, apiendpoint, apiversion):
    global total, fail, success
    total += 1
    if(apiendpoint is True):
        siteurl = ("http://localhost:5000/catalog/api/" + apiversion)
    else:
        siteurl = ("http://localhost:5000/catalog")
    try:
        h = Http()
        url = siteurl + url
        resp, content = h.request(
            url, 'GET', headers={
                "Content-Type": "application/json"})
        if resp['status'] != '200':
            print bcolors.FAIL + (url + ' status code of %s ' % resp['status'])
            fail += 1
        else:
            print bcolors.OKGREEN + (url + ' is ok!')
            success += 1
    except Exception as err:
        print bcolors.FAIL + url + " FAILED "
        print err.args
        sys.exit()


print "Running Endpoint Tester....\n"


# TEST WWW endpoints
print bcolors.OKBLUE + "WWW Endpoints\n"
endpointTester("", False, "none")

print bcolors.OKBLUE + "+ Category Endpoints\n"
endpointTester("/category/1/edit/", False, "none")
endpointTester("/add", False, "none")
endpointTester("/1/delete/", False, "none")

print bcolors.OKBLUE + "+ SubCategory Endpoints\n"
endpointTester("/subcategory/1/add/", False, "none")
endpointTester("/subcategory/1/edit/", False, "none")
endpointTester("/subcategory/1/delete/", False, "none")
endpointTester("/subcategory/1", False, "none")

print bcolors.OKBLUE + "+ ItemCategory Endpoints\n"
endpointTester("/itemcategory/1/1/add/", False, "none")
endpointTester("/itemcategory/1/edit/", False, "none")
endpointTester("/itemcategory/1/delete/", False, "none")
endpointTester("/itemcategory/1", False, "none")

print bcolors.OKBLUE + "+ Item Endpoints\n"
endpointTester("/items/1", False, "none")
endpointTester("/item/1", False, "none")
endpointTester("/item/1/1/1/add/", False, "none")
endpointTester("/item/1/delete", False, "none")
endpointTester("/item/1/edit", False, "none")

print bcolors.OKBLUE + "+ Other Endpoints\n"
endpointTester("/1/myitems/", False, "none")
endpointTester("/settings/admin", False, "none")
endpointTester("/accessdenied", False, "none")

# TEST API endpoints
print bcolors.OKBLUE + "API Endpoints\n"
endpointTester("/item/1/JSON", True, "v1.0")
endpointTester("/category/1/JSON", True, "v1.0")
endpointTester("/category/1/subcategorys/JSON", True, "v1.0")
endpointTester("/subcategory/1/JSON", True, "v1.0")
endpointTester("/subcategory/1/itemcategorys/JSON", True, "v1.0")
endpointTester("/itemcategory/1/JSON", True, "v1.0")
endpointTester("/itemcategory/1/items/JSON", True, "v1.0")


# print summary
print bcolors.OKBLUE + "\nSummary Endpoint Tester"

if(fail > 0):
    print bcolors.FAIL + ("\n + endpoint tester validated " +
                          str(success) + "/" + str(total) + " urls")
    print (" + endpoint tester found " + str(fail) + " bad urls")
    print bcolors.OKBLUE + ("")
else:
    print bcolors.OKGREEN + ("\n + endpoint tester validated " +
                             str(success) + "/" + str(total) + " urls")