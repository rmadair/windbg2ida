Import debugging traces from WinDBG into IDA. Color the graph, fill in the value of all operands, etc.

From WinDBG:

1. Open a log file, ".logopen mylog.txt"
2. Step through a program manually or automatically, "pa 0xdeadbeef"
3. In IDA, import the windbg2ida.py file
4. In the output window, "windbg2ida(mylog.txt)"
