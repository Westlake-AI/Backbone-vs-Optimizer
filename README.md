<div align="center">
<h2><a href="https://github.com/Westlake-AI/Backbone-vs-Optimizer">A Decade’s Battle on Bias of Visual Backbone and Optimizer</a></h2>

[Siyuan Li](https://lupin1998.github.io/)<sup>\*,1,2</sup>, [Juanxi Tian](https://openreview.net/profile?id=~Juanxi_Tian1)<sup>\*,1</sup>, [Zedong Wang](https://zedongwang.netlify.app/)<sup>\*,1</sup>, [Luyuan Zhang](https://openreview.net/profile?id=~Luyuan_Zhang1)<sup>1</sup>, [Zicheng Liu](https://pone7.github.io/)<sup>1</sup>, [Chen Tan](https://chengtan9907.github.io/)<sup>1</sup>, [Weiyang Jin](https://openreview.net/profile?id=~Weiyang_Jin1)<sup>1</sup>, [Lei Xin](https://openreview.net/profile?id=~Lei_Xin2)<sup>1</sup>, [Yang Liu](https://scholar.google.co.id/citations?user=t1emSE0AAAAJ&hl=zh-CN)<sup>2</sup>, [Baigui Sun](https://scholar.google.co.id/citations?user=ZNhTHywAAAAJ&hl=zh-CN)<sup>2</sup>, [Stan Z. Li](https://scholar.google.com/citations?user=Y-nyLGIAAAAJ&hl=zh-CN)<sup>†,1</sup>

<sup>1</sup>[Westlake University](https://westlake.edu.cn/), <sup>2</sup>[Damo Academy](https://damo.alibaba.com/?language=en)
</div>

<!-- Introduction -->

## Introduction

The past decade has witnessed rapid progress in vision backbones and an evolution of deep optimizers from SGD to Adam variants. This paper, for the first time, delves into the relationship between vision network design and optimizer selection. We conduct comprehensive benchmarking studies on mainstream vision backbones and widely-used optimizers, revealing an intriguing phenomenon termed *backbone-optimizer coupling bias* (BOCB). Notably, classical ConvNets, such as VGG and ResNet, exhibit a marked co-dependency with SGD, while modern architectures, including ViTs and ConvNeXt, demonstrate a strong coupling with optimizers with adaptive learning rates like AdamW. More importantly, we uncover the adverse impacts of BOCB on popular backbones in real-world practice, such as additional tuning time and resource overhead, which indicates the remaining challenges and even potential risks. Through in-depth analysis and apples-to-apples comparisons, however, we surprisingly observe that specific types of network architecture can significantly mitigate BOCB, which might serve as promising guidelines for future backbone design. We hope this work as a kick-start can inspire the community to further question the long-held assumptions on vision backbones and optimizers, consider BOCB in future studies, and thus contribute to more robust, efficient, and effective vision systems. It is time to go beyond those usual choices and confront the elephant in the room. The source code and models are publicly available.

<p align="center">
<img src="https://github.com/Westlake-AI/SEMA/assets/44519745/9cca9ed6-2f77-4dc9-972d-84e30ac66a64" width=100% 
class="center">
</p>

## Catalog

This repo is mainly based on [OpenMixup](https://github.com/Westlake-AI/openmixup) to implement image classification tasks while using [MMDetection](https://github.com/open-mmlab/mmdetection/) for transfer learning tasks. **The manuscript and repo are updating, please watch us for the latest release!**

- [x] **Image Classification** on CIFAR-100 and ImageNet-1K in [OpenMixup](https://github.com/Westlake-AI/openmixup/tree/main/configs/classification/cifar100/). [[configs](classification/)]
- [ ] **Object Detection and Segmentation** on COCO. [[code](detection/)]
- [ ] **Trained Models** on CIFAR-100, ImageNet-1K, and COCO.

## Installation
Please check [INSTALL.md](./openmixup/docs/en/install.md) for installation instructions.

## Experimental Results

<p align="center">
<img src="https://github.com/Westlake-AI/SEMA/assets/44519745/3d83bca2-a688-4aee-baf7-072c94398b8f" width=95% 
class="center">
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

## License

This project is released under the [Apache 2.0 license](LICENSE).

## Acknowledgement

Our implementation is mainly based on the following codebases. We gratefully thank the authors for their wonderful works.

- [OpenMixup](https://github.com/Westlake-AI/openmixup): Open-source toolbox for visual representation learning.
- [MMDetection](https://github.com/open-mmlab/mmdetection): OpenMMLab Detection Toolbox and Benchmark.

## Citation

If you find this repository helpful, please consider citing:
```
@article{li2024battle,
  title={A Decade’s Battle on Bias of Visual Backbone and Optimizer},
  author={Siyuan Li and Juanxi Tian and Zedong Wang and Luyuan Zhang and Zicheng Liu and Cheng Tan and Weiyang Jin and Lei Xin and Yang Liu and Baigui Sun and Stan Z. Li},
  year={2024},
}
```

<p align="right">(<a href="#top">back to top</a>)</p>
