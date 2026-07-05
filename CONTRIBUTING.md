# 🤝 Contribution — L'ÉVEIL NOCTURNE

> *Le serment du mouvement :*
> ***Je ne cache pas. Je ne détruis pas. Je ne mens pas. Je ne gates pas.***

---

## 🎯 Qui peut contribuer ?

**N'importe qui.**

Pas de niveau minimum. Pas de diplôme. Pas de "tu dois d'abord apprendre X". Si t'as :
- La curiosité
- L'éthique
- La discipline de l'approfondir

→ **T'es des nôtres.**

---

## 🛤️ Comment contribuer

### 🐛 Reporter un bug

1. Vérifie qu'il n'est pas déjà reporté (search dans Issues)
2. Crée une Issue avec :
   - Titre clair (`[BUG] ghosteye_proxy crash sur port 8082`)
   - OS + version Python + version ffmpeg
   - Commandes exécutées
   - Output complet (pas juste "ça marche pas")
   - Screenshot si UI

### 💡 Proposer une feature

1. Crée une Discussion (pas une Issue)
2. Explique le **pourquoi** avant le **quoi**
3. Liste les alternatives envisagées (divergence)
4. Propose un PoC si possible

### 🔧 Soumettre un PR

**Règles non négociables :**
- Lis **tout le code** que tu touches avant de le modifier
- Teste sur **2 OS minimum** (Linux + un autre)
- Documente chaque ajout dans le README/INSTALL/USAGE
- Signe ton commit (`Signed-off-by: Ton Nom <email@>`)
- Pas de dépendance cachée — si t'ajoutes un pip package, justifie-le
- Pas de breaking change sans discussion préalable

**Template de PR :**
```markdown
## Quoi
[Description courte]

## Pourquoi
[Le problème résolu / la feature ajoutée]

## Comment
[Approche technique]

## Tests effectués
- [ ] OS1: ...
- [ ] OS2: ...
- [ ] Cas limites: ...

## Screenshots
[Si UI]
```

### 📚 Écrire un tutoriel

Suit la **structure 7-sections obligatoire** (voir [PROTOCOL.md](PROTOCOL.md)) :

```
1. PHILOSOPHIE   → pourquoi cette technique existe
2. PRÉREQUIS     → ce que tu dois savoir
3. THÉORIE       → comment ça marche VRAIMENT
4. PRATIQUE      → commande par commande, output attendu
5. PIÈGES        → ce qui va casser, comment éviter
6. ALTERNATIVES  → 2-3 autres approches
7. TRANSMISSION  → exercise : trouve X, fais Y, publie Z
```

**Section 7 non négociable** — c'est la transmission qui crée la scène.

### 🌍 Traduire

- FR (canadien/européen) → prioritaire
- EN → obligatoire pour la diffusion
- ES, DE, PT, AR, ZH → bienvenues

Traduit un README, un tuto, ou le Manifeste.

### 🔒 Disclosure responsable

Tu as trouvé une 0-day ?

1. **NE PUBLIE PAS** sur Issues publiques
2. Contacte : `ghost1o1 [at] proton [dot] me`
3. Laisse 90 jours au vendor pour patcher
4. Coordonnes la publication après le patch

---

## 🚫 Ce qu'on n'accepte PAS

- Code sans doc
- PR qui break sans test de régression
- "Je sais pas coder mais j'ai une idée" sans PoC
- Spam, pub, self-promo hors-sujet
- Attaques sur des systèmes non autorisés (dans issues, c'est un ban immédiat)
- Drama, ego, clanisme

---

## 🎖️ Reconnaissance

Tes contributions sont **nommées** :
- Dans le CHANGELOG
- Dans la section Contributors du README
- Sur le site hub si t'es contributeur régulier

**Tu ne contribues pas dans l'anonymat. Tu signes ton œuvre.**

---

## 📜 Code de Conduite

L'ÉVEIL NOCTURNE est un mouvement **inclusif** :
- Pas de discrimination (race, genre, orientation, classe, neuro, etc.)
- Pas de harcèlement
- Pas de gatekeeping
- Pas de condescendance

**Le savoir se partage. Point.**

Tout comportement contraire = ban.

---

## 🔥 Le serment à signer (optionnel mais apprécié)

Avant ton premier PR ou ta première Issue, copie-colle ce serment en commentaire :

```
✦ SERMENT L'ÉVEIL NOCTURNE ✦

Je, [ton nom/pseudo], reconnais que :
- Je ne cache pas. Je documente et partage.
- Je ne détruis pas. Je teste sur mes cibles ou je signale.
- Je ne mens pas. Je dis "je ne sais pas" quand c'est le cas.
- Je ne gates pas. Le savoir est un commons.

Signé le [date], pour le mouvement L'ÉVEIL NOCTURNE.
```

→ Ce n'est pas une obligation juridique. C'est un **rappel à toi-même** de ce que tu défends.

---

## 📞 Contact

- **GitHub Issues** : pour tout ce qui est technique
- **GitHub Discussions** : pour les idées, questions, annonces
- **Proton Mail** (clé PGP sur demande) : pour la disclosure 0-day

---

<div align="center">

**L'ÉVEIL NOCTURNE** · [ghost1o1](https://github.com/187Ghost101) — 2026

*There is no lock. Du silence naît la lumière.*

</div>
