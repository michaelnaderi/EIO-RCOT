import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11})
INK="#1f2937"; MUTED="#6b7280"
SEC={"Manufacturing":"#2563eb","Construction":"#d97706","Agriculture":"#16a34a"}

# ---------- 1. workflow ----------
fig,ax=plt.subplots(figsize=(12,3.4),dpi=200); ax.set_xlim(0,12); ax.set_ylim(0,3.4); ax.axis("off")
steps=[("SysML model","BDD + ACT\n(form & function)","#e0e7ff","#3730a3"),
       ("HFGT toolbox","XML input  →\nincidence tensors $\\widetilde{\\mathcal{M}}_\\rho^{\\pm}$","#dbeafe","#1d4ed8"),
       ("Matricization","Python reader  →\n$M = M^+ - M^-$  (5×6)","#dcfce7","#15803d"),
       ("HFNMCF / RCOT","Julia · JuMP · HiGHS\nmin $\\pi'F^*U$  s.t. $MU\\geq C$","#fef3c7","#b45309")]
w,h,gap,x0,y0=2.55,2.1,0.42,0.25,0.75
for i,(t,sub,fc,ec) in enumerate(steps):
    x=x0+i*(w+gap)
    ax.add_patch(FancyBboxPatch((x,y0),w,h,boxstyle="round,pad=0.02,rounding_size=0.18",fc=fc,ec=ec,lw=1.6))
    ax.text(x+w/2,y0+h-0.42,f"{i+1}. {t}",ha="center",va="center",fontsize=12.5,weight="bold",color=ec)
    ax.text(x+w/2,y0+0.78,sub,ha="center",va="center",fontsize=10.2,color=INK,linespacing=1.5)
    if i<3: ax.annotate("",xy=(x+w+gap-0.04,y0+h/2),xytext=(x+w+0.04,y0+h/2),arrowprops=dict(arrowstyle="-|>",lw=1.8,color=MUTED))
ax.text(6,0.3,"Output: firing vector $U$ (= RCOT technology outputs $x^*$), objective $Z$, factor use $\\phi = F^*U$",ha="center",fontsize=10.5,color=MUTED)
fig.savefig("figures/workflow.png",bbox_inches="tight",facecolor="white"); plt.close()

# ---------- 2. incidence matrix ----------
M=np.array([[0.65,-0.15,-0.23,-0.26,-0.28,-0.24],[-0.25,0.78,0.84,-0.22,-0.21,-0.25],
            [-0.20,-0.26,-0.30,0.69,0.67,0.70],[-2.10,-3.20,-1.90,-1.20,-0.80,-1.40],[-1.20,-2.20,-1.30,-1.30,-1.10,-1.10]])
rows=["Manufactured\nproduct","Construction\nproduct","Agricultural\nproduct","Capital","Water"]
cols=["Man.","Cons.\nconv.","Cons.\nmodern","Ag.\nlabor","Ag.\nhybrid","Ag.\nautomated"]
fig,ax=plt.subplots(figsize=(8.2,5.2),dpi=200)
lim=3.2; im=ax.imshow(M,cmap="RdBu",vmin=-lim,vmax=lim,aspect="auto")
for i in range(5):
    for j in range(6):
        v=M[i,j]; ax.text(j,i,f"{v:.2f}",ha="center",va="center",fontsize=11,color="white" if abs(v)>1.6 else INK,weight="bold" if v>0 else None)
ax.set_xticks(range(6)); ax.set_xticklabels(cols,fontsize=10); ax.set_yticks(range(5)); ax.set_yticklabels(rows,fontsize=10)
ax.xaxis.tick_top(); ax.axhline(2.5,color=INK,lw=2)
ax.text(6.0,1,"$\\mathcal{I}^*-A^*$\n(n × T)",va="center",ha="left",fontsize=11,color=INK)
ax.text(6.0,3.5,"$-F^*$\n(k × T)",va="center",ha="left",fontsize=11,color=INK)
ax.set_title("Hetero-functional incidence matrix  $M = M^+ - M^-$  (5 × 6)",pad=48,fontsize=13,weight="bold",color=INK)
for s in ax.spines.values(): s.set_visible(False)
fig.savefig("figures/incidence_matrix.png",bbox_inches="tight",facecolor="white"); plt.close()

# ---------- 3. results ----------
U=[99.7883,0,87.5364,0,26.6439,71.9531]
lab=["Manufacturing","Construction\nconventional","Construction\nmodern","Agriculture\nlabor-based","Agriculture\nhybrid","Agriculture\nautomated"]
sec=["Manufacturing","Construction","Construction","Agriculture","Agriculture","Agriculture"]
fig,(a1,a2)=plt.subplots(1,2,figsize=(12,4.6),dpi=200,gridspec_kw=dict(width_ratios=[2.3,1]))
b=a1.bar(range(6),U,color=[SEC[s] for s in sec],edgecolor=[SEC[s] for s in sec],lw=1.4)
for bar,u,s in zip(b,U,sec):
    if u==0: bar.set_facecolor("white"); bar.set_hatch("///")
    a1.text(bar.get_x()+bar.get_width()/2,max(u,0)+2.5,f"{u:.2f}" if u else "not selected",ha="center",fontsize=9.5,color=INK if u else MUTED)
a1.set_xticks(range(6)); a1.set_xticklabels(lab,fontsize=9.5); a1.set_ylabel("Firing / output  $U = x^*$"); a1.set_ylim(0,115)
a1.set_title("Optimal technology choice",loc="left",weight="bold",color=INK)
for sp in ["top","right"]: a1.spines[sp].set_visible(False)
use=[497.92,342.00]; cap=[540,342]; un=["million $","million gal"]
for i,(u,c,n) in enumerate(zip(use,cap,un)):
    pct=100*u/c
    a2.barh(i,100,color="#e5e7eb",height=0.5); a2.barh(i,pct,color="#dc2626" if pct>=99.99 else "#475569",height=0.5)
    a2.text(103,i,f"{pct:.1f}%"+("  binding" if pct>=99.99 else ""),va="center",fontsize=10,weight="bold",color=INK)
    a2.text(1.5,i+0.36,f"{u:.2f} of {c} {n}",va="center",fontsize=8.8,color=MUTED)
a2.set_yticks([0,1]); a2.set_yticklabels(["Capital","Water"]); a2.invert_yaxis(); a2.set_xlim(0,140); a2.set_xticks([])
a2.set_title("Factor utilization (% of availability)",loc="left",weight="bold",color=INK)
for sp in ["top","right","bottom"]: a2.spines[sp].set_visible(False)
fig.suptitle("Minimum price-weighted factor use:  Z = 805.7241",x=0.5,y=1.02,fontsize=12.5,color=INK)
fig.tight_layout(); fig.savefig("figures/results.png",bbox_inches="tight",facecolor="white"); plt.close()
