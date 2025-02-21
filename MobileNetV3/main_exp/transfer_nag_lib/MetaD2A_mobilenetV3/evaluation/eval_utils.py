import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.utils
from transfer_nag_lib.MetaD2A_mobilenetV3.evaluation.codebase.data_providers.aircraft import FGVCAircraft
from transfer_nag_lib.MetaD2A_mobilenetV3.evaluation.codebase.data_providers.pets2 import PetDataset
import torch.utils.data as Data
from transfer_nag_lib.MetaD2A_mobilenetV3.evaluation.codebase.data_providers.autoaugment import CIFAR10Policy


def get_dataset(data_name, batch_size, data_path, num_workers,
                img_size, autoaugment, cutout, cutout_length):
	num_class_dict = {
		'cifar100': 100,
		'cifar10': 10,
		'mnist': 10,
		'aircraft': 100,
		'svhn': 10,
		'pets': 37
	}
		# 'aircraft30': 30,
		# 'aircraft100': 100,
	
	train_transform, valid_transform = _data_transforms(
     		data_name, img_size, autoaugment, cutout, cutout_length)
	if data_name == 'cifar100':
		train_data = torchvision.datasets.CIFAR100(
			root=data_path, train=True, download=True, transform=train_transform)
		valid_data = torchvision.datasets.CIFAR100(
			root=data_path, train=False, download=True, transform=valid_transform)
	elif data_name == 'cifar10':
		train_data = torchvision.datasets.CIFAR10(
			root=data_path, train=True, download=True, transform=train_transform)
		valid_data = torchvision.datasets.CIFAR10(
			root=data_path, train=False, download=True, transform=valid_transform)
	elif data_name.startswith('aircraft'):
		print(data_path)
		if 'aircraft100' in data_path:
			data_path = data_path.replace('aircraft100', 'aircraft/fgvc-aircraft-2013b')
		else:
			data_path = data_path.replace('aircraft', 'aircraft/fgvc-aircraft-2013b')
		train_data = FGVCAircraft(data_path, class_type='variant', split='trainval',
		                          transform=train_transform, download=True)
		valid_data = FGVCAircraft(data_path, class_type='variant', split='test',
		                          transform=valid_transform, download=True)
	elif data_name.startswith('pets'):
		train_data = PetDataset(data_path, train=True, num_cl=37,
		                        val_split=0.15, transforms=train_transform)
		valid_data = PetDataset(data_path, train=False, num_cl=37,
		                        val_split=0.15, transforms=valid_transform)
	else:
		raise KeyError
	
	train_queue = torch.utils.data.DataLoader(
		train_data, batch_size=batch_size, shuffle=True, pin_memory=True,
		num_workers=num_workers)
	
	valid_queue = torch.utils.data.DataLoader(
		valid_data, batch_size=200, shuffle=False, pin_memory=True,
		num_workers=num_workers)
	
	return train_queue, valid_queue, num_class_dict[data_name]



class Cutout(object):
	def __init__(self, length):
		self.length = length
	
	def __call__(self, img):
		h, w = img.size(1), img.size(2)
		mask = np.ones((h, w), np.float32)
		y = np.random.randint(h)
		x = np.random.randint(w)
		
		y1 = np.clip(y - self.length // 2, 0, h)
		y2 = np.clip(y + self.length // 2, 0, h)
		x1 = np.clip(x - self.length // 2, 0, w)
		x2 = np.clip(x + self.length // 2, 0, w)
		
		mask[y1: y2, x1: x2] = 0.
		mask = torch.from_numpy(mask)
		mask = mask.expand_as(img)
		img *= mask
		return img


def _data_transforms(data_name, img_size, autoaugment, cutout, cutout_length):
	if 'cifar' in data_name:
		norm_mean = [0.49139968, 0.48215827, 0.44653124]
		norm_std = [0.24703233, 0.24348505, 0.26158768]
	elif 'aircraft' in data_name:
		norm_mean = [0.48933587508932375, 0.5183537408957618, 0.5387914411673883]
		norm_std = [0.22388883112804625, 0.21641635409388751, 0.24615605842636115]
	elif 'pets' in data_name:
		norm_mean = [0.4828895122298728, 0.4448394893850807, 0.39566558230789783]
		norm_std = [0.25925664613996574, 0.2532760018681693, 0.25981017205097917]
	else:
		raise KeyError
	
	train_transform = transforms.Compose([
		transforms.Resize((img_size, img_size), interpolation=Image.BICUBIC),  # BICUBIC interpolation
		transforms.RandomHorizontalFlip(),
	])
	
	if autoaugment:
		train_transform.transforms.append(CIFAR10Policy())
	
	train_transform.transforms.append(transforms.ToTensor())
	
	if cutout:
		train_transform.transforms.append(Cutout(cutout_length))
	
	train_transform.transforms.append(transforms.Normalize(norm_mean, norm_std))
	
	valid_transform = transforms.Compose([
		transforms.Resize((img_size, img_size), interpolation=Image.BICUBIC),  # BICUBIC interpolation
		transforms.ToTensor(),
		transforms.Normalize(norm_mean, norm_std),
	])
	return train_transform, valid_transform
