# -*- coding: utf-8 -*-
'''
Created on 4 cze 2014

@author: Katarzyna Krasnowska
'''

def get_prepnp_sem_obls(prepnp):
    ret = prepnp_sem_obls.get(prepnp, set([]))
    if prepnp == u'prepnp(przez,bier)':
        ret.add('OBL-AG')
    return ret

prepnp_sem_obls = {
# z Walentego
u'prepnp(bez,dop)' : set(['OBL-MOD']),
u'prepnp(do,dop)' : set(['OBL-ADL', 'OBL-DUR']),
u'prepnp(dokoła,dop)' : set(['OBL-LOCAT']),
u'prepnp(dookoła,dop)' : set(['OBL-LOCAT']),
u'prepnp(jak,str)' : set(['OBL-MOD']),
u'prepnp(jako,str)' : set(['OBL-MOD']),
u'prepnp(koło,dop)' : set(['OBL-LOCAT', 'OBL-TEMP']),
u'prepnp(ku,cel)' : set(['OBL-ADL']),
u'prepnp(między,bier)' : set(['OBL-ADL']),
u'prepnp(między,narz)' : set(['OBL-LOCAT', 'OBL-PERL', 'OBL-TEMP']),
u'prepnp(na,bier)' : set(['OBL-ADL']),
u'prepnp(na,miej)' : set(['OBL-LOCAT']),
u'prepnp(nad,bier)' : set(['OBL-ADL']),
u'prepnp(nad,narz)' : set(['OBL-LOCAT', 'OBL-PERL']),
u'prepnp(naokoło,dop)' : set(['OBL-LOCAT']),
u'prepnp(naokół,dop)' : set(['OBL-LOCAT']),
u'prepnp(naprzeciw,dop)' : set(['OBL-LOCAT']),
u'prepnp(o,miej)' : set(['OBL-TEMP']),
u'prepnp(obok,dop)' : set(['OBL-LOCAT', 'OBL-PERL']),
u'prepnp(od,dop)' : set(['OBL-ABL', 'OBL-DUR']),
u'prepnp(około,dop)' : set(['OBL-TEMP']),
u'prepnp(po,miej)' : set(['OBL-PERL', 'OBL-TEMP']),
u'prepnp(pod,bier)' : set(['OBL-ADL', 'OBL-MOD']),
u'prepnp(pod,narz)' : set(['OBL-LOCAT', 'OBL-PERL']),
u'prepnp(podczas,dop)' : set(['OBL-TEMP']),
u'prepnp(pomiędzy,bier)' : set(['OBL-ADL']),
u'prepnp(pomiędzy,narz)' : set(['OBL-LOCAT', 'OBL-PERL', 'OBL-TEMP']),
u'prepnp(ponad,narz)' : set(['OBL-LOCAT', 'OBL-PERL']),
u'prepnp(poniżej,dop)' : set(['OBL-LOCAT']),
u'prepnp(popod,narz)' : set(['OBL-LOCAT']),
u'prepnp(poprzez,bier)' : set(['OBL-PERL']),
u'prepnp(powyżej,dop)' : set(['OBL-LOCAT']),
u'prepnp(poza,bier)' : set(['OBL-ADL']),
u'prepnp(poza,narz)' : set(['OBL-LOCAT']),
u'prepnp(pośrodku,dop)' : set(['OBL-LOCAT']),
u'prepnp(pośród,dop)' : set(['OBL-LOCAT']),
u'prepnp(przed,bier)' : set(['OBL-ADL']),
u'prepnp(przed,narz)' : set(['OBL-LOCAT', 'OBL-TEMP']),
u'prepnp(przez,bier)' : set(['OBL-DUR', 'OBL-PERL']),
u'prepnp(przy,miej)' : set(['OBL-LOCAT']),
u'prepnp(spod,dop)' : set(['OBL-ABL']),
u'prepnp(spomiędzy,dop)' : set(['OBL-ABL']),
u'prepnp(sponad,dop)' : set(['OBL-ABL']),
u'prepnp(spopod,dop)' : set(['OBL-ABL']),
u'prepnp(spoza,dop)' : set(['OBL-ABL']),
u'prepnp(sprzed,dop)' : set(['OBL-ABL']),
u'prepnp(u,dop)' : set(['OBL-LOCAT']),
u'prepnp(w,bier)' : set(['OBL-ADL', 'OBL-TEMP']),
u'prepnp(w,miej)' : set(['OBL-LOCAT']),
u'prepnp(wewnątrz,dop)' : set(['OBL-LOCAT']),
u'prepnp(wkoło,dop)' : set(['OBL-LOCAT']),
u'prepnp(wokół,dop)' : set(['OBL-LOCAT']),
u'prepnp(wpośród,dop)' : set(['OBL-LOCAT']),
u'prepnp(wzdłuż,dop)' : set(['OBL-LOCAT', 'OBL-PERL']),
u'prepnp(wśród,dop)' : set(['OBL-LOCAT']),
u'prepnp(z,dop)' : set(['OBL-ABL']),
u'prepnp(z,narz)' : set(['OBL-MOD']),
u'prepnp(za,bier)' : set(['OBL-ADL']),
u'prepnp(za,narz)' : set(['OBL-LOCAT']),
u'prepnp(znad,dop)' : set(['OBL-ABL']),
u'prepnp(zza,dop)' : set(['OBL-ABL']),
u'prepnp(śród,dop)' : set(['OBL-LOCAT']),
}