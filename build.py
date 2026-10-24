"""Rebuild the standalone horizontal ebook from approved content and cover."""
import pathlib,json,re,html,base64
P=pathlib.Path(__file__).parent
B=json.loads((P/'content.json').read_text())
esc=html.escape
toc=[];sections=[]
for c in B['chapters']:
 toc.append(dict(id=c['id'],no=c['no'],title=esc(c['title']),eyebrow='',grp=None))
 body=[];in_list=False
 for b in c['blocks']:
  kind=b['type'];t=b['text']
  if kind!='li' and in_list:body.append('</ul>');in_list=False
  if kind=='li':
   if not in_list:body.append('<ul class="book-list">');in_list=True
   body.append('<li>'+esc(t.lstrip('・'))+'</li>')
  elif kind in ['h2','h3']:
   text=t[1:-1] if t.startswith('〔') and t.endswith('〕') else t
   body.append('<'+kind+' class="book-'+kind+'">'+esc(text)+'</'+kind+'>')
  elif kind=='score_table':
   rows=''.join('<tr><th scope="row">第'+str(i+1)+'章</th><td>'+x+'</td><td>　／20</td></tr>' for i,x in enumerate(['判断軸','お金','住まい','万が一','老後','健康','災害']))
   body.append('<table class="score-table"><caption>人生診断 章別スコア記入欄</caption><thead><tr><th>章</th><th>項目</th><th>得点</th></tr></thead><tbody>'+rows+'<tr><th colspan="2">合計</th><td>　／140</td></tr></tbody></table>')
  else:body.append('<p class="say'+(' checklist' if kind=='check' else '')+'">'+esc(t)+'</p>')
 if in_list:body.append('</ul>')
 sections.append('<section id="'+c['id']+'"><p class="eyebrow">'+esc(c['no'])+'</p><h1>'+esc(c['title'])+'</h1>\n'+'\n'.join(body)+'\n</section>')
s=(P/'template.html').read_text()
s=s.replace('{{BODY}}','\n'.join(sections)).replace('{{TOC}}',json.dumps(toc,ensure_ascii=False))
s=s.replace('{{COVER}}',base64.b64encode((P/'cover.jpg').read_bytes()).decode())
(P/'index.html').write_text(s)
print('Built index.html:',len(s.encode()),'bytes,',len(sections),'sections')
