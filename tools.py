def writetoaiml(aimlfile,cat):
    out = open(aimlfile,'w')
    out.write('<?xml version="1.0" encoding="utf-8"?>\n')
    out.write('< aiml version = "1.0" >\n')
    out.write("  <category>\n")
    out.write("    <pattern>")
    pat = cat.pattern.encode("utf-8")
    if not pat.strip():
        return
    else:
        pat = pat.replace("&", "&amp;")
        pat = pat.replace("<", "&lt;")
        pat = pat.replace(">", "&gt;")
        pat = pat.replace("'", "&apos;")
        pat = pat.replace('"', "&quot;")
        out.write(pat)
    out.write("</pattern>\n")
    out.write("    <template>\n")
    print cat.pattern
    if len(cat.tempaltes) > 1:
        out.write("      <random>\n")
        for template in cat.tempaltes:
            print template
            out.write("        <li>")
            temp = template.encode("utf-8").replace("&", "&amp;")
            temp = temp.replace("<", "&lt;")
            temp = temp.replace(">", "&gt;")
            temp = temp.replace("'", "&apos;")
            temp = temp.replace('"', "&quot;")
            out.write(temp)
            out.write("</li>\n")
            # count += 1
            out.write("      </random>\n")
    else:
        template = cat.tempaltes("utf-8")
        print template
        temp = template.replace("&", "&amp;")
        temp = temp.replace("<", "&lt;")
        temp = temp.replace(">", "&gt;")
        temp = temp.replace("'", "&apos;")
        temp = temp.replace('"', "&quot;")
        # charset=chardet.detect(words)["encoding"]
        out.write(temp + '\n')
    out.write("    </template>\n")
    out.write("  </category>\n")
    out.write('< /aiml >\n')
    out.flush()
