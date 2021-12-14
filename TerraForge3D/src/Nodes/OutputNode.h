#pragma once
#pragma once

#include "Base/NodeEditor/NodeEditor.h"

class OutputNode : public NodeEditorNode {
public:
	virtual NodeOutput Evaluate(NodeInputParam input);
	virtual void Load(nlohmann::json data);
	virtual nlohmann::json Save();
	virtual void OnRender();
	OutputNode();
};