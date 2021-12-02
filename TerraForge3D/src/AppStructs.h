#pragma once

#include <string.h>
#include <glm/gtc/constants.hpp>
#include <glm/gtc/quaternion.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/ext/matrix_relational.hpp>
#include <glm/ext/vector_relational.hpp>
#include <glm/ext/scalar_relational.hpp>
#include <time.h>
#include <json.hpp>

struct Vec2 {
	float x = 0;
	float y = 0;
};

struct Vec3 {
	float x = 0;
	float y = 0;
	float z = 0;
};

struct Vec4 {
	float x = 0;
	float y = 0;
	float z = 0;
	float w = 0;
};

struct Stats
{
	float deltaTime = 1;
	float frameRate = 1;
	int triangles = 0;
	int vertCount = 0;
};

struct NoiseLayer {

	NoiseLayer() {
		noiseType = (char*)malloc(1024);
		memset(noiseType, 0, 1024);
		strcpy(noiseType, "Simplex Perlin");
		strcpy_s(name, "Noise Layer");
		strength = 0.0f;
		enabled = true;
		active = false;
		scale = 1;
		offsetX = 0;
		offsetY = 0;
		offsetZ = 0;
	}

	nlohmann::json Save() {
		nlohmann::json data;
		data["type"] = std::string(noiseType);
		data["strength"] = strength;
		data["name"] = std::string(name);
		data["scale"] = scale;
		data["offsetX"] = offsetX;
		data["offsetY"] = offsetY;
		data["offsetZ"] = offsetZ;
		data["enabled"] = enabled;
		data["active"] = active;
		return data;
	}

	void Load(nlohmann::json data) {
		if(noiseType)
			delete noiseType;
		noiseType = (char*)malloc(1024);
		memset(noiseType, 0, 1024);
		strcpy(noiseType, std::string(data["type"]).c_str());
		std::string t = std::string(data["name"]);
		memcpy_s(name, 256, t.c_str(), 256);
		strength = data["strength"];
		scale = data["scale"];
		offsetX = data["offsetX"];
		offsetY = data["offsetY"];
		offsetZ = data["offsetZ"];
		enabled = data["enabled"];
		active = data["active"];
	}

	NoiseLayer Clone(){
		NoiseLayer clone;
		if(clone.noiseType)
			delete noiseType;
		clone.noiseType = (char*)malloc(1024);
		memset(clone.noiseType, 0, 1024);
		strcpy(clone.noiseType, noiseType);
		memcpy_s(clone.name, 256, name, 256);
		clone.strength = strength;
		clone.scale = scale;
		clone.offsetX = offsetX;
		clone.offsetY = offsetY;
		clone.offsetZ = offsetZ;
		clone.enabled = enabled;
		clone.active = active;
		return clone;
	}

	char* noiseType;
	char name[256];
	float strength;
	float offsetX, offsetY, offsetZ;
	float scale;
	bool enabled;
	bool active;
};

struct ActiveWindows {
	bool styleEditor = false;
	bool statsWindow = false;
	bool shaderEditorWindow = false;
	bool texturEditorWindow = false;
	bool seaEditor = false;
	bool elevationNodeEditorWindow = false;
	bool contribWindow = false;
	bool textureStore = false;
	bool osLisc = false;
	bool filtersManager = false;
	bool foliageManager = false;
	bool supportersTribute = false;
	bool skySettings = false;
};