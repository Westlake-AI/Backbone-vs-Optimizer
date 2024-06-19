_base_ = [
    '../../_base_/datasets/aircrafts/sz224_bs16.py',
    '../../_base_/default_runtime.py',
]

# pre_conv_cfg or value_neck_cfg
conv1x1=dict(
    type="ConvNeck",
    in_channels=256, hid_channels=128, out_channels=1,  # MixBlock v
    num_layers=2, kernel_size=1,
    with_last_bn=False, norm_cfg=dict(type='BN'),  # ori
    with_last_dropout=0.1, with_avg_pool=False, with_residual=False)

# model settings
model = dict(
    type='AutoMixup',
    pretrained="torchvision://resnet18",
    alpha=2.0,
    momentum=0.999,  # 0.999 to 0.99999
    mask_layer=2,
    mask_loss=0.1,  # using mask loss
    mask_adjust=0,
    lam_margin=0.08,  # degenerate to mixup when lam or 1-lam <= 0.08
    mix_shuffle_no_repeat=True,  # for fine-grained
    debug=False,  # show attention and content map
    backbone=dict(
        type='ResNet',
        depth=18,
        num_stages=4,
        out_indices=(2,3),  # stage-3 for MixBlock, x-1: stage-x
        style='pytorch'),
    mix_block = dict(  # SAMix
        type='PixelMixBlock',
        in_channels=256, reduction=2, use_scale=True,
        unsampling_mode=['bilinear',],  # str or list, train & test MixBlock
        lam_concat=False, lam_concat_v=False,
        lam_mul=True, lam_residual=True, lam_mul_k=1,  # lam: mult + k=1
        value_neck_cfg=conv1x1,  # SAMix: non-linear value
        x_qk_concat=True, x_v_concat=False,  # SAMix: x qk concat
        # att_norm_cfg=dict(type='BN'),  # norm after q,k (design for fp16, also conduct better performace in fp32)
        mask_loss_mode="L1+Variance", mask_loss_margin=0.1,  # L1 + var loss
        frozen=False),
    head_one=dict(
        type='ClsHead',  # default CE
        loss=dict(type='CrossEntropyLoss', use_soft=False, use_sigmoid=False, loss_weight=1.0),
        with_avg_pool=True, multi_label=False, in_channels=512, num_classes=100),
    head_mix=dict(  # backbone & mixblock
        type='ClsMixupHead',  # mixup, default CE
        loss=dict(type='CrossEntropyLoss', use_soft=False, use_sigmoid=False, loss_weight=1.0),
        with_avg_pool=True, multi_label=False, in_channels=512, num_classes=100),
    head_weights=dict(
        head_mix_q=1, head_one_q=1, head_mix_k=1, head_one_k=1),
)

# additional hooks
custom_hooks = [
    dict(type='SAVEHook',
        save_interval=416 * 50,  # 50 ep
        iter_per_epoch=416,
    ),
    dict(type='CustomCosineAnnealingHook',  # 0.1 to 0
        attr_name="mask_loss", attr_base=0.1, by_epoch=False,  # by iter
        min_attr=0.,
    ),
    dict(type='CosineScheduleHook',
        end_momentum=0.99996,
        adjust_scope=[0.1, 1.0],
        warming_up="constant",
        update_interval=1)
]
# optimizer
optimizer = dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0005,
                paramwise_options={
                    'mix_block': dict(lr=0.01, momentum=0.9)},)  # required parawise_option
# optimizer args
optimizer_config = dict(update_interval=1, grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)

# additional scheduler
addtional_scheduler = dict(
    policy='CosineAnnealing', min_lr=5e-4,
    paramwise_options=['mix_block'],
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=200)
