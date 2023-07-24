# RNA_cap

seq = "GGGAATCTTCCGCAATAAAACTCAAAGGAATTTCGATGCAACGCGAAGAACCTTCCCGAAGCCGGTGGCCGACAATCTTCGGCAAT"
ss = "((((((((((((((...(((.((....)).)))...)))...).)))))...)))))..........(((((......)))))..."


curl -X 'GET' \
  'http://127.0.0.1:8000/generate_png/?seq=GGGAATCTTCCGCAATAAAACTCAAAGGAATTTCGATGCAACGCGAAGAACCTTCCCGAAGCCGGTGGCCGACAATCTTCGGCAAT&ss=(((.((....)).)))...)))...'
