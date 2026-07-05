# 🔒 SECURITY — L'ÉVEIL NOCTURNE

> *La preuve remplace la destruction.*

---

## Versions supportées

| Version | Supportée |
|---------|-----------|
| Latest (main) | ✅ Active |
| -1 | ⚠️ Security fixes seulement |
| Plus anciennes | ❌ Non supportées |

---

## 🚨 Reporter une vulnérabilité

**NE PAS** ouvrir d'Issue publique pour les vulnérabilités.

**Contact :** `ghost1o1 [at] proton [dot] me` (PGP sur demande)

**Inclure :**
- Description de la vulnérabilité
- Étapes de reproduction (PoC)
- Impact potentiel
- Versions affectées
- Ta coordonnée (pour follow-up)

**Engagement :**
- Accusé de réception sous **48h**
- Validation sous **7 jours**
- Patch coordonné sous **30-90 jours** selon sévérité
- Crédit dans le CVE + CHANGELOG (sauf demande d'anonymat)

---

## ⚖️ Politique de divulgation

**Divulgation responsable** : 90 jours standard, négociable selon complexité.

**Cas particuliers :**
- **RCE non-auth sur produit grand public** : 7 jours max
- **Backdoor intentionnelle** : immédiate après vendor
- **Data breach active** : coordination avec vendor + autorité légale

---

## 🛡️ Bonnes pratiques pour les utilisateurs

### Lab personnel
- Isole ton lab (VM, VLAN dédié, ou réseau Air-gapped)
- Utilise des **credentials uniques par cible**
- **Sauvegarde** l'état initial avant tout test
- **Logs horodatés** de chaque action

### Production
- **Jamais** d'outil offensif sur un système de prod sans fenêtre de maintenance
- Toujours informer l'équipe IT/Sécu
- Avoir un **rollback plan** documenté
- **Coordination** avec le SOC si présent

### Légal
- **Autorisation écrite** obligatoire pour toute cible non-personnelle
- Cibles d'entraînement : HackTheBox, TryHackMe, DVWA, OWASP, CTF
- **Pas d'attaque** sur des infrastructures de tiers sans mandat

---

## 🔐 Security du repo lui-même

### Branches protégées
- `main` : pas de push direct, PR obligatoire
- `release/*` : figée après release

### Secrets
- **Aucun** token ou credential dans le code
- Utilise `.env` (non commité) ou vault
- Tous les secrets de test sont **fake** ou clairement marqués

### CI/CD
- Scan de dépendances automatisé (Dependabot)
- Lint obligatoire avant merge
- Tests unitaires requis pour les modules critiques

### Dependances
- Minimum de dépendances tierces
- Toutes vérifiées manuellement avant ajout
- Pas de supply chain obscure

---

## 📋 Signaler un abus

Si tu vois quelqu'un utiliser L'ÉVEIL NOCTURNE pour :
- Attaquer des systèmes non autorisés
- Du black-hat non-éthique
- Du drama / doxxing / harcèlement

→ Contacte-nous. **On ne protège pas les abuseurs.**

---

## 🏅 Remerciements

Contributeurs sécurité (avec permission) :
- [Liste vide pour l'instant — sois le premier]

---

<div align="center">

**L'ÉVEIL NOCTURNE** · [ghost1o1](https://github.com/187Ghost101) — 2026

*Là où l'ignorance dort, nous allumons.*

</div>
