_base_ = [
    '../../_base_/models/deepcluster/r18.py',
    '../../_base_/datasets/cifar100/deepcluster_sz224_bs64.py',
    '../../_base_/default_runtime.py',
]

# interval for accumulate gradient
update_interval = 1

# optimizer
optimizer = dict(type='SGD', lr=0.03, weight_decay=1e-4, momentum=0.9)

# fp16
use_fp16 = False
fp16 = dict(type='mmcv', loss_scale='dynamic')
# optimizer args
optimizer_config = dict(update_interval=update_interval, grad_clip=None)

# learning policy
lr_config = dict(policy='step', step=[120, 160])

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=1000)
