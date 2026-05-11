# -*- coding: utf-8 -*-
"""
Created on Mon May 11 23:04:17 2026

@author: yanni
"""
import geometrie as gm

el = gm.ellipse(100, 75, 50, 0.9,0.3)
l0 = el.ligne(0)
l1 = el.ligne(2.7)
l0.angle(l1)

gm.affichage()