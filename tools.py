def writetoaiml(self):
    global out, count
    out.write("  <category>\n")
    out.write("    <pattern>")
    words = self.question.encode("utf-8")
    if not words.strip():
        return
    words = words.replace("&", "&amp;")
    words = words.replace("<", "&lt;")
    words = words.replace(">", "&gt;")
    words = words.replace("'", "&apos;")
    words = words.replace('"', "&quot;")
    out.write(words)
    out.write("</pattern>\n")
    out.write("    <template>\n")
    print self.question
    if len(self.answers) > 1:
        out.write("      <random>\n")
        for x in self.answers:
            print x
            out.write("        <li>")
            words = x.encode("utf-8").replace("&", "&amp;")
            words = words.replace("<", "&lt;")
            words = words.replace(">", "&gt;")
            words = words.replace("'", "&apos;")
            words = words.replace('"', "&quot;")
            out.write(words)
            out.write("</li>\n")
            # count += 1
            out.write("      </random>\n")
    else:
        x = self.answer.encode("utf-8")
        print x
        words = x.replace("&", "&amp;")
        words = words.replace("<", "&lt;")
        words = words.replace(">", "&gt;")
        words = words.replace("'", "&apos;")
        words = words.replace('"', "&quot;")
        # charset=chardet.detect(words)["encoding"]
        out.write(words + '\n')
    out.write("    </template>\n")
    out.write("  </category>\n")
    out.flush()
    count += 1
    print count
    # self.content=set()