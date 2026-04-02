import scanpy as sc
import json
import matplotlib.pyplot as plt




def load_data(file_path, box):
    adata = sc.read(file_path, n_jobs=12)
    adata.uns = {}

    # maxvalue = adata.X.max()
    # if maxvalue > 10:
    #     sc.pp.log1p(adata)

    adata.obs['RD1'] = adata.obsm[metadata[box]['obsm']][:, 0]
    adata.obs['RD2'] = adata.obsm[metadata[box]['obsm']][:, 1]

    lst_order = adata.obs[metadata[box]['type']].unique()
    adata.obs['celltype'] = adata.obs[metadata[box]['type']].astype('category').cat.set_categories(lst_order)

    # st.session_state['counter'] += 1
    # st.write(f"counter: {st.session_state['counter']}")

    return adata



if __name__ == "__main__":
        
    with open("frontend/data/metadata.json", 'r', encoding='utf-8') as file:
        metadata = json.load(file)
    adata = load_data('frontend/data/pig_testis.h5ad', 'pig_testis')

    gene_list = adata.var_names
    print(gene_list)
    print(len(gene_list))
    print(type(gene_list.tolist()))

    exit(0)

    sc.pl.umap(adata, color=['celltype_qin'], show=False, save='_pig_testis_celltype_qin.png')
    sc.pl.umap(adata, color=['KIT',], show=False, save='_pig_testis_gene.png')

    ax = sc.pl.violin(adata, ['KIT',], groupby='celltype_qin', show=False)

    # 旋转 x 轴标签
    plt.xticks(rotation=45, ha='right')
    # 或者使用 ax 对象
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    # 调整布局
    plt.tight_layout()
    # 手动保存
    plt.savefig('figures/violin_pig_testis_gene_violin.png', bbox_inches='tight', dpi=300)
    plt.close()